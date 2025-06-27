import composants.*;


import javax.naming.event.ObjectChangeListener;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class GamePanel extends JPanel implements ActionListener {

    Timer timer;
    Parametres mySettings = new Parametres();
    ContainerBox mainBox = new ContainerBox("main", mySettings, null);
    Object focusComponent;
    int[] MouseCoo = {0, 0};
    String preLoad;

    GamePanel(String[] args) {
        int largeur = 1280;
        int hauteur = 720;
        if (args.length > 0) {
            preLoad = args[0];
        }
        this.setPreferredSize(new Dimension(largeur, hauteur));
        this.setBackground(new Color(0, 0, 0));
        this.setFocusable(true);
        this.addKeyListener(new MyKeyAdapter());
        this.addMouseListener(new MyMouseListener());
        StartGame();
    }
    public void StartGame() {
        timer = new Timer(0, this);
        timer.start();

        mainBox.addObject("background", "ContainerBox", 0, 0, 1280, 720);
        ((ContainerBox) mainBox.getObject("background")).setBackgroundColor(Color.white);

        ((ContainerBox) mainBox.getObject("background")).addObject("main table", "SplitSlideBar", 20, 80, 845, 600);
        ((ContainerBox) mainBox.getObject("background")).addObject("main list", "ContainerBox", 885, 20, 365, 600);
        ((ContainerBox) mainBox.getObject("main list")).setColumn(2);
        ((ContainerBox) mainBox.getObject("main list")).setBackgroundColor(mySettings.mainTheme.secondaryColor);

        new BUTTON("", mySettings, null).createNewPage((SplitSlideBar) mainBox.getObject("main table"), (ContainerBox) mainBox.getObject("main list"));


        ((ContainerBox) mainBox.getObject("background")).addObject("button add page", "BUTTON", "Nouvelle page", 885, 640, 180, 60, -1, -1);
        ((BUTTON) mainBox.getObject("button add page")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((BUTTON) mainBox.getObject("button add page")).setCommand(mainBox.getObject("main table"), 7, mainBox.getObject("main list"));
        ((ContainerBox) mainBox.getObject("background")).addObject("button remove page", "BUTTON", "Supprimer la page", 1070, 640, 180, 60, -1, -1);
        ((BUTTON) mainBox.getObject("button remove page")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((BUTTON) mainBox.getObject("button remove page")).setCommand(mainBox.getObject("main table"), 8);

        ((ContainerBox) mainBox.getObject("main list")).addObject("perso manager", "FloatingBox", 5, 5, 175, 250);
        ((ContainerBox) mainBox.getObject("perso manager")).setBackgroundColor(mySettings.mainTheme.mainColor);
        ((ContainerBox) mainBox.getObject("perso manager")).addObject("button add perso", "BUTTON", "Créer un nouveau personnage", -1, 20, 150, 100, -1, -1);
        ((BUTTON) mainBox.getObject("button add perso")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((BUTTON) mainBox.getObject("button add perso")).setCommand((mainBox.getObject("main list")), 5);
        ((ContainerBox) mainBox.getObject("perso manager")).addObject("button remove perso", "BUTTON", "Supprimer un personnage", -1, 130, 150, 100, -1, -1);
        ((BUTTON) mainBox.getObject("button remove perso")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((BUTTON) mainBox.getObject("button remove perso")).setCommand((mainBox.getObject("main list")), 6, mainBox.getObject("main table"));

        ((ContainerBox) mainBox.getObject("background")).addObject("save", "BUTTON", "Save", 20, 20, 420, 40, -1, -1);
        ((BUTTON) mainBox.getObject("save")).setCommand(mainBox, 9);
        ((ContainerBox) mainBox.getObject("background")).addObject("load", "BUTTON", "Load", 445, 20, 420, 40, -1, -1);
        ((BUTTON) mainBox.getObject("load")).setCommand(mainBox, 10);
        if (Objects.nonNull(preLoad)) {
            ((BUTTON) mainBox.getObject("load")).setCommand(mainBox, 10, preLoad);
            ((BUTTON) mainBox.getObject("load")).Pressed();
        }
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        drawComponents(g);
    }
    public void drawComponents(Graphics g) {
        mainBox.getSettings().rapportX = (float) this.getWidth() / 1280;
        mainBox.getSettings().rapportY = (float) this.getHeight() / 720;
        mainBox.getSettings().rapportM = (mainBox.getSettings().rapportX + mainBox.getSettings().rapportY) / 2;
        mainBox.draw(g);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            if (!Arrays.equals(MouseCoo, new int[] {}) && Objects.nonNull(focusComponent) && Objects.nonNull(this.getMousePosition())) {
                if (focusComponent.getClass() == TEXTZONE.class) {
                    int delta = (int) (MouseCoo[1] - this.getMousePosition().getY());
                    if (!((TEXTZONE) focusComponent).getSlider().isSens()) {
                        delta = (int) (MouseCoo[0] - this.getMousePosition().getX());
                    }
                    ((TEXTZONE) focusComponent).getSlider().addPourcent(delta);
                } else if (focusComponent.getClass() == TEXT.class) {
                    int delta = (int) (MouseCoo[1] - this.getMousePosition().getY());
                    if (!((TEXT) focusComponent).getSlider().isSens()) {
                        delta = (int) (MouseCoo[0] - this.getMousePosition().getX());
                    }
                    ((TEXT) focusComponent).getSlider().addPourcent(delta);
                } else if (focusComponent.getClass() == ContainerBox.class) {
                    int delta = (int) (MouseCoo[1] - this.getMousePosition().getY());
                    if (!((ContainerBox) focusComponent).getSlider().isSens()) {
                        delta = (int) (MouseCoo[0] - this.getMousePosition().getX());
                    }
                    ((ContainerBox) focusComponent).getSlider().addPourcent(delta);
                } else if (focusComponent.getClass() == SplitSlideBar.class) {
                    int delta = (int) (MouseCoo[0] - this.getMousePosition().getX());
                    ((SplitSlideBar) focusComponent).addDepassement(-delta);
                }
                MouseCoo[0] = (int) this.getMousePosition().getX();
                MouseCoo[1] = (int) this.getMousePosition().getY();
            }
        } catch (NullPointerException err) {
            err.printStackTrace();
        }
        Map<Object, Integer> allComposants = getAllComponent(mainBox, 0);
        for (Object obj : allComposants.keySet()) {
            if (focusComponent != obj) {
                if (obj.getClass() == TEXT.class ) {
                    if (((TEXT) obj).getName().contains("perso description zone")) {
                        String start = ((TEXT) obj).getName().replace("perso description zone", "");
                        ((TEXT) obj).setText(mainBox.getSettings().allPersonnages.get(((TEXT) ((TEXT) obj).getParent().getObject(start + "perso name")).getText()).description);
                    }
                } else if (obj.getClass() == TEXTZONE.class ) {
                    if (((TEXTZONE) obj).getName().contains("fiche description zone")) {
                        String start = ((TEXTZONE) obj).getName().replace("fiche description zone", "");
                        ((TEXTZONE) obj).setText(mainBox.getSettings().allPersonnages.get(((TEXT) ((TEXTZONE) obj).getParent().getObject(start + "fiche name")).getText()).description);
                    }
                }
            }
        }
        repaint();
    }
    public class MyKeyAdapter extends KeyAdapter {

        @Override
        public void keyPressed(KeyEvent e) {
            super.keyPressed(e);
            if (Objects.nonNull(focusComponent)) {
                if (focusComponent.getClass() == TEXTZONE.class) {
                    TEXTZONE objet = (TEXTZONE) focusComponent;
                    if (e.getKeyCode() == 8) {
                        objet.removeLetter(objet.getText().length() - 1);
                    } else {
                        for (char l : mainBox.getSettings().possibleLetter.toCharArray()) {
                            if (e.getKeyChar() == l) {
                                if (l != '\n' || objet.isNewLine()) {
                                    objet.addLetter(e.getKeyChar(), objet.getText().length());
                                } else {
                                    focusComponent = null;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    public class MyMouseListener extends MouseAdapter {
        @Override
        public void mouseClicked(MouseEvent e) {
            float rapX = mainBox.getSettings().rapportX;
            float rapY = mainBox.getSettings().rapportY;
            super.mouseClicked(e);
            int mouseX = e.getX();
            int mouseY = e.getY();

            int maxDeep = 0;
            Map<Object, Integer> allComposants = getAllComponent(mainBox, 0);
            for (Object obj : allComposants.keySet()) {
                if (allComposants.get(obj) > maxDeep) {
                    maxDeep = allComposants.get(obj);
                }
            }
            for (int i = 0; i <= maxDeep; i++) {
                for (Object obj : allComposants.keySet()) {
                    if (allComposants.get(obj) == i) {
                        if (obj.getClass() == BUTTON.class) {
                            BUTTON objet = (BUTTON) obj;
                            if (objet.getPosX()*rapX < mouseX && mouseX < objet.getPosX()*rapX + objet.getSizeX()*rapX && objet.getPosY()*rapY < mouseY && mouseY < objet.getPosY()*rapY + objet.getSizeY()*rapY) {
                                objet.Pressed();
                            }
                        }
                    }
                }
            }
        }

        @Override
        public void mousePressed(MouseEvent e) {
            float rapX = mainBox.getSettings().rapportX;
            float rapY = mainBox.getSettings().rapportY;
            super.mousePressed(e);
            int mouseX = e.getX();
            int mouseY = e.getY();
            MouseCoo = new int[] {mouseX, mouseY};

            if (Objects.nonNull(focusComponent)) {
                if (focusComponent.getClass() == TEXTZONE.class) {
                    if (((TEXTZONE) focusComponent).getName().contains("fiche description zone")) {
                        String start = ((TEXTZONE) focusComponent).getName().replace("fiche description zone", "");
                        String name = ((TEXT) ((TEXTZONE) focusComponent).getParent().getObject(start + "fiche name")).getText();
                        mainBox.getSettings().allPersonnages.get(name).description = ((TEXTZONE) focusComponent).getText();
                    }
                }
            }

            int maxDeep = 0;
            Map<Object, Integer> allComposants = getAllComponent(mainBox, 0);
            for (Object obj : allComposants.keySet()) {
                if (allComposants.get(obj) > maxDeep) {
                    maxDeep = allComposants.get(obj);
                }
            }
            for (int i = 0; i <= maxDeep; i++) {
                for (Object obj : allComposants.keySet()) {
                    if (allComposants.get(obj) == i) {
                        if (obj.getClass() == TEXTZONE.class) {
                            TEXTZONE objet = (TEXTZONE) obj;
                            if (objet.getPosX()*rapX < mouseX && mouseX < objet.getPosX()*rapX + objet.getSizeX()*rapX && objet.getPosY()*rapY < mouseY && mouseY < objet.getPosY()*rapY + objet.getSizeY()*rapY) {
                                focusComponent = obj;
                            }
                        } else if (obj.getClass() == TEXT.class) {
                            TEXT objet = (TEXT) obj;
                            if (objet.getPosX()*rapX < mouseX && mouseX < objet.getPosX()*rapX + objet.getSizeX()*rapX && objet.getPosY()*rapY < mouseY && mouseY < objet.getPosY()*rapY + objet.getSizeY()*rapY) {
                                focusComponent = obj;
                            }
                        } else if (obj.getClass() == IMAGE.class) {
                            IMAGE objet = (IMAGE) obj;
                            if (objet.getPosX()*rapX < mouseX && mouseX < objet.getPosX()*rapX + objet.getSizeX()*rapX && objet.getPosY()*rapY < mouseY && mouseY < objet.getPosY()*rapY + objet.getSizeY()*rapY) {
                                focusComponent = obj;
                            }
                        } else if (obj.getClass() == BUTTON.class) {
                            BUTTON objet = (BUTTON) obj;
                            if (objet.getPosX()*rapX < mouseX && mouseX < objet.getPosX()*rapX + objet.getSizeX()*rapX && objet.getPosY()*rapY < mouseY && mouseY < objet.getPosY()*rapY + objet.getSizeY()*rapY) {
                                focusComponent = obj;
                            }
                        } else if (obj.getClass() == ContainerBox.class) {
                            ContainerBox objet = (ContainerBox) obj;
                            if (objet.getPosX()*rapX < mouseX && mouseX < objet.getPosX()*rapX + objet.getSizeX()*rapX && objet.getPosY()*rapY < mouseY && mouseY < objet.getPosY()*rapY + objet.getSizeY()*rapY) {
                                focusComponent = obj;
                            }
                        } else if (obj.getClass() == SplitSlideBar.class) {
                            SplitSlideBar objet = (SplitSlideBar) obj;
                            if (objet.getPosX()*rapX < mouseX && mouseX < objet.getPosX()*rapX + objet.getSizeX()*rapX && objet.getPosY()*rapY + objet.getSizeY()*rapY < mouseY && mouseY < objet.getPosY()*rapY + objet.getSizeY()*rapY + objet.getWidth()*rapY) {
                                focusComponent = obj;
                            }
                        }
                    }
                }
            }
        }

        @Override
        public void mouseReleased(MouseEvent e) {
            super.mouseReleased(e);
            if (Objects.nonNull(focusComponent)) {
                if (focusComponent.getClass() == SplitSlideBar.class) {
                    ((SplitSlideBar) focusComponent).resetDepassement();
                }
            }
            MouseCoo = new int[] {};
        }
    }

    public Map<Object, Integer> getAllComponent(ContainerBox box, int deep) {
        Map<Object, Integer> result = new HashMap<>();
        for (Object obj : box.getContenu()) {
            result.put(obj, deep);
            if (obj.getClass() == ContainerBox.class) {
                result.put(obj, deep);
                Map<Object, Integer> newBox = getAllComponent((ContainerBox) obj, deep+1);
                for (Object newObj: newBox.keySet()) {
                    result.put(newObj, newBox.get(newObj));
                }
            } else if (obj.getClass() == FloatingBox.class) {
                ContainerBox Container = ((FloatingBox) obj).getContenu();
                result.put(Container, deep);
                Map<Object, Integer> newBox = getAllComponent(Container, deep+1);
                for (Object newObj: newBox.keySet()) {
                    result.put(newObj, newBox.get(newObj));
                }
            } else if (obj.getClass() == SplitSlideBar.class) {
                ContainerBox Container = ((SplitSlideBar) obj).getContenu();
                result.put(Container, deep);
                Map<Object, Integer> newBox = getAllComponent(Container, deep+1);
                for (Object newObj: newBox.keySet()) {
                    result.put(newObj, newBox.get(newObj));
                }
            } else {
                result.put(obj, deep);
            }
        }
        return result;
    }
}
