package composants;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.filechooser.FileFilter;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.plaf.DesktopPaneUI;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class BUTTON extends JFrame {

    String name;
    Parametres mySettings;
    ContainerBox parent;
    int marginX;
    int marginY;
    int sizeX;
    int sizeY;
    int paddingX = 5;
    int paddingY = 5;
    Color backgroundColor = Color.white;
    Color foregroundColor = Color.black;
    Font myFont;
    String Text = "";
    BufferedImage myImage;
    Image drawImage;
    boolean centerX = false;
    boolean centerY = false;
    boolean reductible = false;
    Object actionneur;
    int action;
    Object[] parametersAction;

    float lastRapportX = 0;
    float lastRapportY = 0;
    String lastPath = "";

    public BUTTON(String name, Parametres settings, ContainerBox parent, int... parametres) {
        setName(name);
        mySettings = settings;
        setMyFont(mySettings.mainTheme.mainFont);
        this.parent = parent;
        if (parametres.length != 0) {
            setMarginX(parametres[0]);
            setMarginY(parametres[1]);
            setSizeX(parametres[2]);
            setSizeY(parametres[3]);
            if (parametres.length > 4) {
                setCenterX(parametres[4] == -1);
            }
            if (parametres.length > 5) {
                setCenterY(parametres[5] == -1);
            }
        }
    }
    public BUTTON(String name, Parametres settings, ContainerBox parent, String text, int... parametres) {
        setName(name);
        mySettings = settings;
        setMyFont(mySettings.mainTheme.mainFont);
        this.parent = parent;
        if (parametres.length != 0) {
            setMarginX(parametres[0]);
            setMarginY(parametres[1]);
            setSizeX(parametres[2]);
            setSizeY(parametres[3]);
            if (parametres.length > 4) {
                setCenterX(parametres[4] == -1);
            }
            if (parametres.length > 5) {
                setCenterY(parametres[5] == -1);
            }
        }
        setText(text);
        if (text.contains("\\")) {
            setImage();
        }
    }
    public BUTTON() {}

    public static BufferedImage loadImage(String path) {
        try {
            return ImageIO.read(new File(path));
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Impossible de load l'image");
        }
        return null;
    }
    public static BufferedImage setImageSize(BufferedImage originalImage, int targetWidth, int targetHeight) {
        Image resultingImage = originalImage.getScaledInstance(targetWidth, targetHeight, Image.SCALE_DEFAULT);
        BufferedImage outputImage = new BufferedImage(targetWidth, targetHeight, BufferedImage.TYPE_INT_ARGB);
        outputImage.getGraphics().drawImage(resultingImage, 0, 0, null);
        return outputImage;
    }
    public static Image replaceColors(Image source, Color search, Color replace) {
        ImageFilter filter = new RGBImageFilter() {
            public int filterRGB(int x, int y, int rgb) {
                if (rgb == search.getRGB()) {
                    return replace.getRGB();
                } else {
                    return rgb;
                }
            }
        };
        ImageProducer ip = new FilteredImageSource(source.getSource(), filter);
        Image image = Toolkit.getDefaultToolkit().createImage(ip);
        BufferedImage bufferedImage = new BufferedImage(image.getWidth(null), image.getHeight(null), BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = bufferedImage.createGraphics();
        g2.setBackground(new Color(0, 0, 0, 0) );
        g2.clearRect(0, 0, 200, 40);
        g2.drawImage(image, 0, 0, null);
        g2.dispose();
        return bufferedImage;
    }

    public void draw(Graphics g) {
        int pX = (int) (getPosX() * mySettings.rapportX);
        int pY = (int) (getPosY() * mySettings.rapportY);
        int sX = (int) (getSizeX() * mySettings.rapportX);
        int sY = (int) (getSizeY() * mySettings.rapportY);
        int mX = (int) (getPaddingX() * mySettings.rapportX);
        int mY = (int) (getPaddingY() * mySettings.rapportY);
        if (centerY) {
            mY = 0;
        }

        g.setColor(getBackgroundColor());
        g.fillRect(pX, pY, sX, sY);


        if (Objects.nonNull(getImage())) {
            if (getName().contains("button perso image")) {
                if (!lastPath.equals(mySettings.allPersonnages.get(((TEXT) parent.getObject(0)).getText()).path)) {
                    lastPath = mySettings.allPersonnages.get(((TEXT) parent.getObject(0)).getText()).path;
                    setText(lastPath);
                    setImage();
                    drawImage = setImageSize((BufferedImage) getImage(), sX, sY);
                }
            }
            if (mySettings.rapportX != lastRapportX || mySettings.rapportY != lastRapportY) {
                drawImage = setImageSize((BufferedImage) getImage(), sX, sY);
                lastRapportX = mySettings.rapportX;
                lastRapportY = mySettings.rapportY;
            }
            g.drawImage(drawImage, pX, pY, null);
        } else {
            g.setColor(getForegroundColor());
            setFontSize((int) (mySettings.mainTheme.mainFont.getSize() * mySettings.rapportM));
            g.setFont(getMyFont());
            FontMetrics metrics = g.getFontMetrics(g.getFont());

            if (isReductible()) {
                while (splitText(getText(), metrics).size() * getMyFont().getSize() > getSizeY()) {
                    setFontSize(getMyFont().getSize()-1);
                    g.setFont(getMyFont());
                    metrics = g.getFontMetrics(g.getFont());
                }
            }
            ArrayList<String> texts = splitText(getText(), metrics);

            int indexLine = 0;
            for (String line : texts) {
                if (mY + metrics.getHeight() * indexLine + metrics.getHeight() / 1.5 < sY && mY + metrics.getHeight() * indexLine >= 0) {
                    int addX = 0;
                    if (isCenterX()) {
                        addX = (sX - metrics.stringWidth(line)) / 2;
                    }
                    int addY = 0;
                    if (isCenterY()) {
                        addY = (sY - (mY + metrics.getHeight() * texts.size())) / 2;
                    }
                    g.drawString(line, pX + mX + addX, (int) (pY + mY + metrics.getHeight() / 1.5 + metrics.getHeight() * indexLine + addY));
                }
                indexLine++;
            }
        }
        g.setColor(Color.black);
        g.drawRect(pX, pY, sX, sY);
    }
    public ArrayList<String> splitText(String message, FontMetrics metrics) {
        int sX = (int) (getSizeX() * mySettings.rapportX);
        int mX = (int) (getPaddingX() * mySettings.rapportX);
        ArrayList<String> myTextSplit = new ArrayList<>();

        for (String paragraphe : message.split("\n")) {
            myTextSplit.add("");
            for (String mot : paragraphe.split(" ")) {
                if (metrics.stringWidth(mot) > sX - 2 * mX) {
                    for (char l : mot.toCharArray()) {
                        if (metrics.stringWidth(myTextSplit.get(myTextSplit.size() - 1) + l) >= sX - 2 * mX) {
                            myTextSplit.add("");
                        }
                        myTextSplit.set(myTextSplit.size() - 1, myTextSplit.get(myTextSplit.size() - 1) + l);
                    }
                    myTextSplit.set(myTextSplit.size() - 1, myTextSplit.get(myTextSplit.size() - 1) + " ");
                } else {
                    if (metrics.stringWidth(myTextSplit.get(myTextSplit.size() - 1) + mot) >= sX - 2 * mX) {
                        myTextSplit.add("");
                    }
                    myTextSplit.set(myTextSplit.size() - 1, myTextSplit.get(myTextSplit.size() - 1) + mot + " ");
                }
            }
        }
        return myTextSplit;
    }

    public void Pressed() {
        if (getAction() == 3) {
            addFichePerso((ContainerBox) getActionneur(), (ContainerBox) getParametersAction()[0]);
        } else if (getAction() == 4) {
            deleteFichePerso((ContainerBox) getActionneur(), (String) getParametersAction()[0]);
        } else if (getAction() == 5) {
            createPersonnage((ContainerBox) getActionneur());
        } else if (getAction() == 6) {
            deletePersonnage((ContainerBox) getActionneur(), (SplitSlideBar) getParametersAction()[0]);
        } else if (getAction() == 7) {
            createNewPage((SplitSlideBar) getActionneur(), (ContainerBox) getParametersAction()[0]);
        } else if (getAction() == 8) {
            deletePage((SplitSlideBar) getActionneur());
        } else if (getAction() == 9) {
            saveGame((ContainerBox) getActionneur());
        } else if (getAction() == 10) {
            loadGame((ContainerBox) getActionneur());
        } else if (getAction() == 11) {
            downloadImage((BUTTON) getActionneur());
        }
    }
    public void saveGame(ContainerBox obj) {
        JFrame jFrame = new JFrame();

        String path = null;
        JFileChooser chooser = new JFileChooser();
        chooser.setDialogTitle("Choisir un emplacement de sauvegarde");
        chooser.setCurrentDirectory(new File(mySettings.pathLoad));
        if (chooser.showSaveDialog(null) == JFileChooser.APPROVE_OPTION) {
            path = chooser.getSelectedFile().getAbsolutePath();
            path = path.replace(".rsmlvr", "");
        }
        if (path != null) {
            mySettings.pathLoad = path;
            try {
                File myObj = new File(path + ".rsmlvr");
                ArrayList<String> s = sauvegarder(obj, 0);
                Map<String, String> images = sauvegarderImage(obj);
                s.add(mySettings.save());
                for (String img : images.keySet()) {
                    s.add(img + ":" + images.get(img));
                }
                FileWriter myWriter = new FileWriter(myObj);
                for (String l : s) {
                    myWriter.write(l);
                    myWriter.write("\n");
                }
                myWriter.close();
                JOptionPane.showMessageDialog(jFrame, "Sauvegarde réussie");
            } catch (IOException e) {
                JOptionPane.showMessageDialog(jFrame, "Sauvegarde échouée");
                e.printStackTrace();
            }
        }
    }
    public void loadGame(ContainerBox main) {
        JFrame jFrame = new JFrame();
        String path = null;
        JFileChooser chooser = new JFileChooser();
        chooser.addChoosableFileFilter(new FileNameExtensionFilter("RSMLVR Document", "rsmlvr"));
        chooser.setAcceptAllFileFilterUsed(true);
        chooser.setDialogTitle("Ouvrir un fichier");
        chooser.setCurrentDirectory(new File(mySettings.pathLoad));
        if (getParametersAction().length != 0) {
            path = (String) getParametersAction()[0];
        } else {
            if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
                path = chooser.getSelectedFile().getAbsolutePath();
            }
        }
        if (path != null) {
            try {
                File myObj = new File(path);

                // Charger les paramètres :
                Scanner myReader = new Scanner(myObj);
                Parametres newSettings = new Parametres();
                newSettings.pathLoad = path;
                newSettings.pathImage = mySettings.pathImage;
                while (myReader.hasNextLine()) {
                    String data = myReader.nextLine();
                    String[] nameObject = data.split(":");
                    if (nameObject[0].length() == 0) {
                        String last = nameObject[0];
                        for (String element : nameObject) {
                            switch (last) {
                                case "Theme" -> {
                                    String[] tab = element.split("\\|");
                                    newSettings.mainTheme.mainColor = new Color(Integer.parseInt(tab[0]), Integer.parseInt(tab[1]), Integer.parseInt(tab[2]));
                                    newSettings.mainTheme.secondaryColor = new Color(Integer.parseInt(tab[3]), Integer.parseInt(tab[4]), Integer.parseInt(tab[5]));
                                    newSettings.mainTheme.tertiaryColor = new Color(Integer.parseInt(tab[6]), Integer.parseInt(tab[7]), Integer.parseInt(tab[8]));
                                }
                                case "Personnage" -> {
                                    String[] tab = element.split("\\|");
                                    System.out.println(Arrays.toString(tab));
                                    for (int i = 0; i < tab.length; i += 3) {
                                        newSettings.allPersonnages.put(tab[i], new Parametres.Personnage(tab[i]));
                                        newSettings.allPersonnages.get(tab[i]).path = tab[i+1];
                                        if (i+2 == tab.length) {
                                            newSettings.allPersonnages.get(tab[i]).description = "";
                                        } else {
                                            newSettings.allPersonnages.get(tab[i]).description = tab[i + 2].replace("\\n", "\n");
                                        }
                                    }
                                }
                            }
                            last = element;
                        }
                        break;
                    }
                }

                // Charger les images :
                myReader = new Scanner(myObj);
                boolean isImage = false;
                while (myReader.hasNextLine()) {
                    String data = myReader.nextLine();
                    String[] nameObject = data.split(":");
                    if (isImage) {
                        try {
                            String[] element = nameObject[1].split("\\|");
                            String extension = element[0];
                            int imgWidth = Integer.parseInt(element[1]);
                            int imgHeight = Integer.parseInt(element[2]);
                            BufferedImage bufferedImage = new BufferedImage(imgWidth, imgHeight, BufferedImage.TYPE_INT_RGB);
                            if (extension.equals("png")) {
                                bufferedImage = new BufferedImage(imgWidth, imgHeight, BufferedImage.TYPE_INT_ARGB);
                            }
                            int lastIndex = 2;
                            int nbIter = 0;
                            int valueRGB = 0;
                            for (int x = 0; x < imgWidth; x++) {
                                for (int y = 0; y < imgHeight; y++) {
                                    if (nbIter == 0) {
                                        lastIndex++;
                                        nbIter = Integer.parseInt(element[lastIndex].split("x")[0]);
                                        valueRGB = Integer.parseInt(element[lastIndex].split("x")[1]);
                                    }
                                    bufferedImage.setRGB(x, y, valueRGB);
                                    nbIter--;
                                }
                            }
                            ImageIO.write(bufferedImage, extension, new File("assets\\images\\" + nameObject[0]));
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    } else if (nameObject[0].length() == 0) {
                        isImage = true;
                    }
                }

                // Charger les composants :
                Map<Integer, Object> arbre = new HashMap<>();
                arbre.put(0, new ContainerBox("main", newSettings, null));

                myReader = new Scanner(myObj);
                while (myReader.hasNextLine()) {
                    String data = myReader.nextLine();
                    String[] nameObject = data.split(":", 3);
                    if (nameObject[0].length() > 0) {
                        int deep = Integer.parseInt(nameObject[0]);
                        for (int i : arbre.keySet()) {
                            if (i == deep - 1) {
                                if (arbre.get(i).getClass() == ContainerBox.class) {
                                    ContainerBox obj = (ContainerBox) arbre.get(i);
                                    String[] parametres = nameObject[2].split("\\|");
                                    if (Objects.equals(nameObject[1], "ContainerBox")) {
                                        obj.addObject(parametres[0], nameObject[1], Integer.parseInt(parametres[1]), Integer.parseInt(parametres[2]), Integer.parseInt(parametres[3]), Integer.parseInt(parametres[4]));
                                        ContainerBox newObj = (ContainerBox) obj.getObject(parametres[0]);
                                        newObj.setRow(Integer.parseInt(parametres[5]));
                                        newObj.setColumn(Integer.parseInt(parametres[6]));
                                        newObj.setBackgroundColor(new Color(Integer.parseInt(parametres[8]), Integer.parseInt(parametres[9]), Integer.parseInt(parametres[10])));
                                        newObj.setSliderBackgroundColor(new Color(Integer.parseInt(parametres[11]), Integer.parseInt(parametres[12]), Integer.parseInt(parametres[13])));
                                        newObj.setSliderForegroundColor(new Color(Integer.parseInt(parametres[14]), Integer.parseInt(parametres[15]), Integer.parseInt(parametres[16])));
                                        newObj.getSlider().setSize(Integer.parseInt(parametres[17]));
                                        newObj.setSliderSens(Boolean.parseBoolean(parametres[18]));
                                        newObj.setSliderVisible(Boolean.parseBoolean(parametres[19]));
                                        arbre.put(deep, newObj);
                                        break;
                                    } else if (Objects.equals(nameObject[1], "SplitSlideBar")) {
                                        obj.addObject(parametres[0], nameObject[1], Integer.parseInt(parametres[1]), Integer.parseInt(parametres[2]), Integer.parseInt(parametres[3]), Integer.parseInt(parametres[4]));
                                        SplitSlideBar newObj = (SplitSlideBar) obj.getObject(parametres[0]);
                                        newObj.setWidth(Integer.parseInt(parametres[5]));
                                        newObj.setSliderBackgroundColor(new Color(Integer.parseInt(parametres[6]), Integer.parseInt(parametres[7]), Integer.parseInt(parametres[8])));
                                        newObj.setSliderForegroundColor(new Color(Integer.parseInt(parametres[9]), Integer.parseInt(parametres[10]), Integer.parseInt(parametres[11])));
                                        newObj.setCursorColor(new Color(Integer.parseInt(parametres[12]), Integer.parseInt(parametres[13]), Integer.parseInt(parametres[14])));
                                        arbre.put(deep, newObj);
                                        break;
                                    } else if (Objects.equals(nameObject[1], "FloatingBox")) {
                                        obj.addObject(parametres[0], nameObject[1], Integer.parseInt(parametres[1]), Integer.parseInt(parametres[2]), Integer.parseInt(parametres[3]), Integer.parseInt(parametres[4]));
                                        ContainerBox newObj = (ContainerBox) obj.getObject(parametres[0]);
                                        newObj.setRow(Integer.parseInt(parametres[5]));
                                        newObj.setColumn(Integer.parseInt(parametres[6]));
                                        newObj.setBackgroundColor(new Color(Integer.parseInt(parametres[8]), Integer.parseInt(parametres[9]), Integer.parseInt(parametres[10])));
                                        newObj.setSliderBackgroundColor(new Color(Integer.parseInt(parametres[11]), Integer.parseInt(parametres[12]), Integer.parseInt(parametres[13])));
                                        newObj.setSliderForegroundColor(new Color(Integer.parseInt(parametres[14]), Integer.parseInt(parametres[15]), Integer.parseInt(parametres[16])));
                                        newObj.getSlider().setSize(Integer.parseInt(parametres[17]));
                                        newObj.setSliderSens(Boolean.parseBoolean(parametres[18]));
                                        newObj.setSliderVisible(Boolean.parseBoolean(parametres[19]));
                                        arbre.put(deep, newObj);
                                        break;
                                    } else if (Objects.equals(nameObject[1], "TEXTZONE")) {
                                        obj.addObject(parametres[0], nameObject[1], parametres[19].replace("\\n", "\n"), Integer.parseInt(parametres[1]), Integer.parseInt(parametres[2]), Integer.parseInt(parametres[3]), Integer.parseInt(parametres[4]));
                                        TEXTZONE newObj = (TEXTZONE) obj.getObject(parametres[0]);
                                        newObj.setPaddingX(Integer.parseInt(parametres[5]));
                                        newObj.setPaddingY(Integer.parseInt(parametres[6]));
                                        newObj.setBackgroundColor(new Color(Integer.parseInt(parametres[7]), Integer.parseInt(parametres[8]), Integer.parseInt(parametres[9])));
                                        newObj.setForegroundColor(new Color(Integer.parseInt(parametres[10]), Integer.parseInt(parametres[11]), Integer.parseInt(parametres[12])));
                                        newObj.setForegroundColorWaiting(new Color(Integer.parseInt(parametres[13]), Integer.parseInt(parametres[14]), Integer.parseInt(parametres[15])));
                                        newObj.setFontName(parametres[16]);
                                        newObj.setFontSize(Integer.parseInt(parametres[17]));
                                        newObj.setFontStyle(Integer.parseInt(parametres[18]));
                                        newObj.setTextWaiting(parametres[20].replace("\\n", "\n"));
                                        newObj.setSliderBackgroundColor(new Color(Integer.parseInt(parametres[21]), Integer.parseInt(parametres[22]), Integer.parseInt(parametres[23])));
                                        newObj.setSliderForegroundColor(new Color(Integer.parseInt(parametres[24]), Integer.parseInt(parametres[25]), Integer.parseInt(parametres[26])));
                                        newObj.getSlider().setSize(Integer.parseInt(parametres[27]));
                                        newObj.setSliderSens(Boolean.parseBoolean(parametres[28]));
                                        newObj.setSliderVisible(Boolean.parseBoolean(parametres[29]));
                                        newObj.setCenter(Boolean.parseBoolean(parametres[30]));
                                        newObj.setNewLine(Boolean.parseBoolean(parametres[31]));
                                    } else if (Objects.equals(nameObject[1], "TEXT")) {
                                        obj.addObject(parametres[0], nameObject[1], parametres[16].replace("\\n", "\n"), Integer.parseInt(parametres[1]), Integer.parseInt(parametres[2]), Integer.parseInt(parametres[3]), Integer.parseInt(parametres[4]));
                                        TEXT newObj = (TEXT) obj.getObject(parametres[0]);
                                        newObj.setPaddingX(Integer.parseInt(parametres[5]));
                                        newObj.setPaddingY(Integer.parseInt(parametres[6]));
                                        newObj.setBackgroundColor(new Color(Integer.parseInt(parametres[7]), Integer.parseInt(parametres[8]), Integer.parseInt(parametres[9])));
                                        newObj.setForegroundColor(new Color(Integer.parseInt(parametres[10]), Integer.parseInt(parametres[11]), Integer.parseInt(parametres[12])));
                                        newObj.setFontName(parametres[13]);
                                        newObj.setFontSize(Integer.parseInt(parametres[14]));
                                        newObj.setFontStyle(Integer.parseInt(parametres[15]));
                                        newObj.setSliderBackgroundColor(new Color(Integer.parseInt(parametres[17]), Integer.parseInt(parametres[18]), Integer.parseInt(parametres[19])));
                                        newObj.setSliderForegroundColor(new Color(Integer.parseInt(parametres[20]), Integer.parseInt(parametres[21]), Integer.parseInt(parametres[22])));
                                        newObj.getSlider().setSize(Integer.parseInt(parametres[23]));
                                        newObj.setSliderSens(Boolean.parseBoolean(parametres[24]));
                                        newObj.setSliderVisible(Boolean.parseBoolean(parametres[25]));
                                        newObj.setCenterX(Boolean.parseBoolean(parametres[26]));
                                        newObj.setCenterY(Boolean.parseBoolean(parametres[27]));
                                        newObj.setReductible(Boolean.parseBoolean(parametres[28]));
                                    } else if (Objects.equals(nameObject[1], "IMAGE")) {
                                        obj.addObject(parametres[0], nameObject[1], parametres[1], Integer.parseInt(parametres[2]), Integer.parseInt(parametres[3]), Integer.parseInt(parametres[4]), Integer.parseInt(parametres[5]));
                                        IMAGE newObj = (IMAGE) obj.getObject(parametres[0]);
                                        newObj.setBackgroundColor(new Color(Integer.parseInt(parametres[6]), Integer.parseInt(parametres[7]), Integer.parseInt(parametres[8])));
                                    } else if (Objects.equals(nameObject[1], "BUTTON")) {
                                        obj.addObject(parametres[0], nameObject[1], parametres[16], Integer.parseInt(parametres[1]), Integer.parseInt(parametres[2]), Integer.parseInt(parametres[3]), Integer.parseInt(parametres[4]));
                                        BUTTON newObj = (BUTTON) obj.getObject(parametres[0]);
                                        newObj.setPaddingX(Integer.parseInt(parametres[5]));
                                        newObj.setPaddingY(Integer.parseInt(parametres[6]));
                                        newObj.setBackgroundColor(new Color(Integer.parseInt(parametres[7]), Integer.parseInt(parametres[8]), Integer.parseInt(parametres[9])));
                                        newObj.setForegroundColor(new Color(Integer.parseInt(parametres[10]), Integer.parseInt(parametres[11]), Integer.parseInt(parametres[12])));

                                        newObj.setFontName(parametres[13]);
                                        newObj.setFontSize(Integer.parseInt(parametres[14]));
                                        newObj.setFontStyle(Integer.parseInt(parametres[15]));
                                        newObj.setCenterX(Boolean.parseBoolean(parametres[17]));
                                        newObj.setCenterY(Boolean.parseBoolean(parametres[18]));
                                        newObj.setReductible(Boolean.parseBoolean(parametres[19]));
                                    }
                                } else if (arbre.get(i).getClass() == SplitSlideBar.class) {
                                    SplitSlideBar obj = (SplitSlideBar) arbre.get(i);
                                    String[] parametres = nameObject[2].split("\\|");
                                    obj.addChild(parametres[0]);
                                    obj.getEnfants().get(obj.getEnfants().size() - 1).setIndex(Integer.parseInt(parametres[1]));
                                    ContainerBox newObj = obj.getEnfant(obj.getEnfants().size() - 1);
                                    newObj.setName(parametres[0]);
                                    newObj.setRow(Integer.parseInt(parametres[2]));
                                    newObj.setColumn(Integer.parseInt(parametres[3]));
                                    newObj.setBackgroundColor(new Color(Integer.parseInt(parametres[5]), Integer.parseInt(parametres[6]), Integer.parseInt(parametres[7])));
                                    newObj.setSliderBackgroundColor(new Color(Integer.parseInt(parametres[8]), Integer.parseInt(parametres[9]), Integer.parseInt(parametres[10])));
                                    newObj.setSliderForegroundColor(new Color(Integer.parseInt(parametres[11]), Integer.parseInt(parametres[12]), Integer.parseInt(parametres[13])));
                                    newObj.getSlider().setSize(Integer.parseInt(parametres[14]));
                                    newObj.setSliderSens(Boolean.parseBoolean(parametres[15]));
                                    newObj.setSliderVisible(Boolean.parseBoolean(parametres[16]));
                                    arbre.put(deep, newObj);
                                    break;
                                }
                                break;
                            }
                        }
                    } else {
                        break;
                    }
                }

                // Actualiser les boutons :
                myReader = new Scanner(myObj);
                String loadName = "load";
                while (myReader.hasNextLine()) {
                    String data = myReader.nextLine();
                    String[] nameObject = data.split(":", 3);
                    if (Objects.equals(nameObject[1], "BUTTON")) {
                        String[] tab = nameObject[2].split("\\|");
                        ArrayList<Object> paramAction = new ArrayList<>();
                        String[] obj = nameObject[2].split("<")[1].split("\\|");
                        for (int i = 0; i < obj.length - 1; i++) {
                            if (Objects.equals(tab[20], "4")) {
                                paramAction.add(obj[i].replace(">", ""));
                            } else {
                                paramAction.add(((ContainerBox) arbre.get(0)).getObject(obj[i]));
                            }
                        }
                        if (Objects.equals(tab[20], "10")) {
                            loadName = tab[0];
                        }
                        ((BUTTON) ((ContainerBox) arbre.get(0)).getObject(tab[0])).setCommand(
                                ((ContainerBox) arbre.get(0)).getObject(tab[21]),
                                Integer.parseInt(tab[20]),
                                paramAction.toArray()
                        );
                    } else if (Objects.equals(nameObject[1], "SplitSlideBar")) {
                        ((SplitSlideBar) ((ContainerBox) arbre.get(0)).getObject(nameObject[2].split("\\|")[0])).setIndexContent(0);
                    } else if (Objects.equals(nameObject[1], "TEXT")) {
                        TEXT obj = (TEXT) ((ContainerBox) arbre.get(0)).getObject(nameObject[2].split("\\|")[0]);
                        if (obj.getName().contains("perso description zone")) {
                            String start = obj.getName().replace("perso description zone", "");
                            System.out.println(((ContainerBox) arbre.get(0)).getSettings().allPersonnages.get(((TEXT) obj.getParent().getObject(start + "perso name")).getText()).description);
                            obj.setText(((ContainerBox) arbre.get(0)).getSettings().allPersonnages.get(((TEXT) obj.getParent().getObject(start + "perso name")).getText()).description);
                            System.out.println(obj.getText());
                        }
                    }
                }

                (main).resetContenu(((ContainerBox) arbre.get(0)).getContenu());
                (main).setSettings(newSettings);
                ((BUTTON) (main).getObject(loadName)).setCommand(getActionneur(), 10);
                myReader.close();
            } catch (FileNotFoundException e) {
                JOptionPane.showMessageDialog(jFrame, "Impossible d'ouvrir le fichier");
                e.printStackTrace();
            }
        }
    }
    public void downloadImage(BUTTON obj) {

            JFrame jFrame = new JFrame();
            String path;
            JFileChooser chooser = new JFileChooser();
            chooser.addChoosableFileFilter(new FileNameExtensionFilter("Images", "jpg", "png", "gif", "bmp"));
            chooser.setAcceptAllFileFilterUsed(true);
            chooser.setDialogTitle("Choisir la photo de profil de " + ((TEXT) obj.parent.getObject(0)).getText());
            chooser.setCurrentDirectory(new File(mySettings.pathImage));
            if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
                path = chooser.getSelectedFile().getAbsolutePath();
                try {
                    mySettings.pathImage = path;
                    Image load = loadImage(path);
                    assert load != null;
                    int nbImage = 0;
                    File[] listFiles = new File("assets\\images").listFiles();
                    ArrayList<Integer> alreadyIn = new ArrayList<>();
                    assert listFiles != null;
                    for (File f : listFiles) {
                        try {
                            alreadyIn.add(Integer.parseInt(f.getPath().split("\\\\")[f.getPath().split("\\\\").length - 1].split("\\.")[0]));
                        } catch (NumberFormatException ignored) {}
                    }
                    for (int i = 0; i <= listFiles.length; i++) {
                        if (!alreadyIn.contains(i)) {
                            nbImage = i;
                            break;
                        }
                    }
                    File output = new File("assets\\images\\" + nbImage + "." + path.split("\\\\")[path.split("\\\\").length - 1].split("\\.")[1]);
                    ImageIO.write((RenderedImage) load, path.split("\\.")[path.split("\\.").length - 1], output);
                    mySettings.allPersonnages.get(((TEXT) obj.parent.getObject(0)).getText()).path = output.getPath();
                } catch (IOException e) {
                    e.printStackTrace();
                    JOptionPane.showMessageDialog(jFrame, "Impossible de charger l'image");
                }
            }
        }

    public void createNewPage(SplitSlideBar obj, ContainerBox listePerso) {
        String nomSplit = String.valueOf(obj.getEnfants().size());

        for (int i = 0; i < obj.getEnfants().size(); i++) {
            boolean hay = false;
            for (SplitBox box : obj.getEnfants()) {
                if (Objects.equals(box.getContenu().getName(), i + "page table")) {
                    hay = true;
                    break;
                }
            }
            if (!hay) {
                nomSplit = String.valueOf(i);
                break;
            }
        }
        int nextIndex = obj.getIndexContent() + 1;

        obj.addChild(nomSplit + "page table");
        ContainerBox page = obj.getEnfant(obj.getEnfants().size()-1);

        for (int i = obj.getEnfants().size()-1; i > nextIndex; i--) {
            SplitBox child1 = obj.getEnfants().get(i);
            obj.getEnfants().set(i, obj.getEnfants().get(i-1));
            obj.getEnfants().set(i-1, child1);
        }

        page.setBackgroundColor(mySettings.mainTheme.mainColor);
        page.setRow(1);
        page.setSliderSens(false);

        page.addObject(nomSplit + "page title", "TEXTZONE", "PAGE " + obj.getEnfants().size(), 0, 0, 845, 40, -1);
        ((TEXTZONE) page.getObject(nomSplit + "page title")).setSliderVisible(false);
        ((TEXTZONE) page.getObject(nomSplit + "page title")).setNewLine(false);
        ((TEXTZONE) page.getObject(nomSplit + "page title")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);

        page.addObject(nomSplit + "add fiche", "FloatingBox", 10, 50, 400, 530);
        ((ContainerBox) page.getObject(nomSplit + "add fiche")).setBackgroundColor(mySettings.mainTheme.secondaryColor);

        ((ContainerBox) page.getObject(nomSplit + "add fiche")).addObject(nomSplit + "button add fiche", "BUTTON", "AJOUTER UN PERSONNAGE", -1, -1, 200, 200, -1, -1);
        ((BUTTON) page.getObject(nomSplit + "button add fiche")).setCommand(page, 3, listePerso);
        ((BUTTON) page.getObject(nomSplit + "button add fiche")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);

        obj.setIndexContent(nextIndex);
    }
    public void deletePage(SplitSlideBar obj) {
        if (obj.getEnfants().size() > 1) {
            obj.getEnfants().remove(obj.getIndexContent());
            obj.setIndexContent(obj.getIndexContent());
        }
    }
    public void addFichePerso(ContainerBox parent, ContainerBox listePerso) {
        ArrayList<String> nomPerso = new ArrayList<>(mySettings.allPersonnages.keySet());
        nomPerso.add("new");
        for (FloatingBox flo : parent.getChild()) {
            for (Object obj : flo.getContenu().getContenu()) {
                if (obj.getClass() == TEXT.class) {
                    if (((TEXT) obj).getName().contains("fiche name")) {
                        nomPerso.remove(((TEXT) obj).getText());
                    }
                }
            }
        }

        String persoName = (String) JOptionPane.showInputDialog(
                null,
                "Quel personnage ajouter ?",
                "Ajouter un personnage",
                JOptionPane.QUESTION_MESSAGE,
                null,
                nomPerso.toArray(),
                nomPerso.get(0));

        if (Objects.nonNull(persoName)) {
            if (persoName.equals("new")) {
                persoName = createPersonnage(listePerso);
            }
            if (Objects.nonNull(persoName)) {
                createNewFichePerso(parent, persoName);
            }
        }
    }
    public void createNewFichePerso(ContainerBox parent, String persoName) {
        StringBuilder start = new StringBuilder(String.valueOf(((SplitBox) parent.parent).getIndex()));
        for (int i = 0; i < parent.getChild().length; i++) {
            boolean hay = false;
            for (FloatingBox ch : parent.getChild()) {
                if (Objects.equals(ch.getContenu().getName(), start.toString() + i + "fiche bloc")) {
                    hay = true;
                    break;
                }
            }
            if (!hay) {
                start.append(i);
                break;
            }
        }
        parent.addObject(start + "fiche bloc", "FloatingBox", 10, 50, 400, 530);
        parent.swapChild(parent.getNbChild()-1, parent.getNbChild()-2);

        ((FloatingBox) parent.getObject(parent.child - 1)).getContenu().setBackgroundColor(mySettings.mainTheme.secondaryColor);
        ((FloatingBox) parent.getObject(parent.child - 1)).getContenu().addObject(start + "button fiche delete", "BUTTON", "assets\\delete.png", 340, 10, 50, 50);
        ((BUTTON) parent.getObject(start + "button fiche delete")).setCommand(parent, 4, start + "fiche bloc");
        ((BUTTON) parent.getObject(start + "button fiche delete")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);

        Parametres.Personnage perso = mySettings.allPersonnages.get(persoName);
        ((FloatingBox) parent.getObject(parent.child - 1)).getContenu().addObject(start + "fiche name", "TEXT", perso.name, 10, 10, 330, 50);
        ((TEXT) parent.getObject(start + "fiche name")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((TEXT) parent.getObject(start + "fiche name")).setReductible(true);
        ((FloatingBox) parent.getObject(parent.child - 1)).getContenu().addObject(start + "fiche image", "IMAGE", perso.path, 260, 60, 130, 150);
        ((IMAGE) parent.getObject(start + "fiche image")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);

        ((FloatingBox) parent.getObject(parent.child - 1)).getContenu().addObject(start + "fiche resume", "TEXTZONE", 10, 220, 380, 300);
        ((TEXTZONE) parent.getObject(start + "fiche resume")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);

        ((FloatingBox) parent.getObject(parent.child - 1)).getContenu().addObject(start + "fiche description", "TEXT", "Description :", 10, 60, 250, 35);
        ((TEXT) parent.getObject(start + "fiche description")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((FloatingBox) parent.getObject(parent.child - 1)).getContenu().addObject(start + "fiche description zone", "TEXTZONE", perso.description, 10, 95, 250, 115);
        ((TEXTZONE) parent.getObject(start + "fiche description zone")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((TEXTZONE) parent.getObject(start + "fiche description zone")).setTextWaiting("Saisir la description...");
    }
    public void deleteFichePerso(ContainerBox obj, String nom) {
        JFrame jFrame = new JFrame();
        ArrayList<Object> contenu = obj.getContenu();
        for (int i = 0; i < contenu.size(); i++) {
            if (contenu.get(i).getClass() == FloatingBox.class) {
                if (Objects.equals(((FloatingBox) contenu.get(i)).getContenu().getName(), nom)) {
                    StringBuilder start = new StringBuilder();
                    for (char l : Arrays.copyOf(nom.toCharArray(), 2)) {
                        start.append(l);
                    }
                    String text = ((TEXT) ((FloatingBox) contenu.get(i)).getContenu().getObject(start + "fiche name")).getText();
                    int result = JOptionPane.showConfirmDialog(jFrame, "Veux-tu vraiment retirer " + text + " ?", "Supprimer ?", JOptionPane.YES_NO_OPTION);
                    if (result == 0) {
                        obj.getContenu().remove(i);
                        obj.child -= 1;
                    }
                    break;
                }
            }
        }
    }
    public String createPersonnage(ContainerBox parent, String... info) {
        JFrame jFrame = new JFrame();
        String nom;
        if (info.length > 0) {
            nom = JOptionPane.showInputDialog(jFrame, info[0] + "Entrer un nom de personnage :", "Choisir un nom", JOptionPane.WARNING_MESSAGE);
        } else {
            nom = JOptionPane.showInputDialog(jFrame, "Entrer un nom de personnage :", "Choisir un nom", JOptionPane.QUESTION_MESSAGE);
        }
        if (Objects.nonNull(nom)) {
            if (nom.toCharArray().length > 0) {
                if (mySettings.allPersonnages.containsKey(nom)) {
                    return createPersonnage(parent, "Le nom existe déjà !\n");
                } else {
                    mySettings.allPersonnages.put(nom, new Parametres.Personnage(nom));
                    createNewPerso(parent, nom);
                    return nom;
                }
            } else {
                return createPersonnage(parent, "Il n'y a pas de nom !\n");
            }
        }
        return null;
    }
    public void createNewPerso(ContainerBox parent, String nom) {

        String start = "";
        for (int i = 0; i < parent.getChild().length; i++) {
            boolean hay = false;
            for (FloatingBox ch : parent.getChild()) {
                if (Objects.equals(ch.getContenu().getName(), i + "list bloc")) {
                    hay = true;
                    break;
                }
            }
            if (!hay) {
                start = String.valueOf(i);
                break;
            }
        }

        parent.addObject(start + "list bloc", "FloatingBox", 5, 5, 175, 250);
        ((ContainerBox) parent.getObject(start + "list bloc")).setBackgroundColor(mySettings.mainTheme.mainColor);
        parent.swapChild(parent.getNbChild()-1, parent.getNbChild()-2);

        ((ContainerBox) parent.getObject(start + "list bloc")).addObject(start + "perso name", "TEXT", nom, 5, 5, 95, 50, -1, -1);
        ((TEXT) parent.getObject(start + "perso name")).setFontSize(15);
        ((TEXT) parent.getObject(start + "perso name")).setFontStyle(Font.BOLD);
        ((TEXT) parent.getObject(start + "perso name")).setReductible(true);
        ((TEXT) parent.getObject(start + "perso name")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);

        ((ContainerBox) parent.getObject(start + "list bloc")).addObject(start + "button perso image", "BUTTON", mySettings.allPersonnages.get(nom).path, 100, 5, 70, 90);
        ((BUTTON) parent.getObject(start + "button perso image")).setCommand(parent.getObject(start + "button perso image"), 11);
        ((BUTTON) parent.getObject(start + "button perso image")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);

        ((ContainerBox) parent.getObject(start + "list bloc")).addObject(start + "perso description", "TEXT", "Description :", 5, 60, 90, 40, 0, -1);
        ((TEXT) parent.getObject(start + "perso description")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((TEXT) parent.getObject(start + "perso description")).setReductible(true);
        ((ContainerBox) parent.getObject(start + "list bloc")).addObject(start + "perso description zone", "TEXT", mySettings.allPersonnages.get(nom).description, 5, 100, 165, 145);
        ((TEXT) parent.getObject(start + "perso description zone")).setBackgroundColor(mySettings.mainTheme.tertiaryColor);
        ((TEXT) parent.getObject(start + "perso description zone")).setSliderVisible(false);
        ((TEXT) parent.getObject(start + "perso description zone")).setReductible(true);
    }
    public void deletePersonnage(ContainerBox parent, SplitSlideBar obj) {

        ArrayList<String> nomPerso = new ArrayList<>(mySettings.allPersonnages.keySet());

        if (nomPerso.size() > 0) {
            String persoName = (String) JOptionPane.showInputDialog(
                    null,
                    "Quel personnage supprimer ?",
                    "Supprimer un personnage",
                    JOptionPane.WARNING_MESSAGE,
                    null,
                    nomPerso.toArray(),
                    nomPerso.get(0));

            if (Objects.nonNull(persoName)) {
                JFrame jFrame = new JFrame();

                ArrayList<Object> contenu = parent.getContenu();
                for (int i = 0; i < contenu.size(); i++) {
                    if (contenu.get(i).getClass() == FloatingBox.class) {
                        if (((FloatingBox) contenu.get(i)).getContenu().getName().contains("list bloc")) {
                            char[] nomP = new char[((FloatingBox) contenu.get(i)).getContenu().getName().length()-"list bloc".length()];
                            System.arraycopy(((FloatingBox) contenu.get(i)).getContenu().getName().toCharArray(), 0, nomP, 0, nomP.length);
                            StringBuilder start = new StringBuilder();
                            for (char l : nomP) {
                                start.append(l);
                            }
                            if (Objects.equals(((TEXT) parent.getObject(start + "perso name")).getText(), persoName)) {
                                int result = JOptionPane.showConfirmDialog(jFrame,
                                        "Veux-tu vraiment supprimer " + persoName + " ?",
                                        "Supprimer ?",
                                        JOptionPane.YES_NO_OPTION, JOptionPane.ERROR_MESSAGE);
                                if (result == 0) {
                                    parent.getContenu().remove(i);
                                    parent.child -= 1;
                                    mySettings.allPersonnages.remove(persoName);
                                    completeRemovePerso(obj, persoName);
                                }
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
    public void completeRemovePerso(SplitSlideBar obj, String nom) {
        for (SplitBox enf : obj.getEnfants()) {
            for (FloatingBox ch : enf.getContenu().getChild()) {
                for (Object o : ch.getContenu().getContenu()) {
                    if (o.getClass() == TEXT.class) {
                        if (((TEXT) o).getName().contains("fiche name")) {
                            if (Objects.equals(((TEXT) o).getText(), nom)) {
                                enf.getContenu().getContenu().remove(ch);
                                enf.getContenu().child--;
                                break;
                            }
                        }
                    }
                }
            }
        }
    }

    public ArrayList<String> sauvegarder(ContainerBox container, int deep) {
        ArrayList<String> sauvegarde = new ArrayList<>();

        for (Object obj : container.getContenu()) {
            if (obj.getClass() == ContainerBox.class) {
                sauvegarde.add(((ContainerBox) obj).save(deep + 1));
                ArrayList<String> s = sauvegarder(((ContainerBox) obj), deep + 1);
                if (Objects.nonNull(s)) {
                    sauvegarde.addAll(s);
                }
            } else if (obj.getClass() == FloatingBox.class) {
                sauvegarde.add(((FloatingBox) obj).save(deep + 1));
                ArrayList<String> s = sauvegarder(((FloatingBox) obj).getContenu(), deep + 1);
                if (Objects.nonNull(s)) {
                    sauvegarde.addAll(s);
                }
            } else if (obj.getClass() == SplitSlideBar.class) {
                sauvegarde.add(((SplitSlideBar) obj).save(deep + 1));
                for (SplitBox split : ((SplitSlideBar) obj).getEnfants()) {
                    sauvegarde.add(split.save(deep + 2));
                    ArrayList<String> s = sauvegarder(split.getContenu(), deep + 2);
                    if (Objects.nonNull(s)) {
                        sauvegarde.addAll(s);
                    }
                }
            } else if (obj.getClass() == TEXT.class) {
                sauvegarde.add(((TEXT) obj).save(deep + 1));
            } else if (obj.getClass() == TEXTZONE.class) {
                sauvegarde.add(((TEXTZONE) obj).save(deep + 1));
            } else if (obj.getClass() == BUTTON.class) {
                sauvegarde.add(((BUTTON) obj).save(deep + 1));
            } else if (obj.getClass() == IMAGE.class) {
                sauvegarde.add(((IMAGE) obj).save(deep + 1));
            }
        }
        return sauvegarde;
    }
    public Map<String, String> sauvegarderImage(ContainerBox container) {
        Map<String, String> images = new HashMap<>();

        for (Object obj : container.getContenu()) {
            if (obj.getClass() == ContainerBox.class) {
                Map<String, String> s = sauvegarderImage(((ContainerBox) obj));
                for (String img : s.keySet()) {
                    images.put(img, s.get(img));
                }
            } else if (obj.getClass() == FloatingBox.class) {
                Map<String, String> s = sauvegarderImage(((FloatingBox) obj).getContenu());
                for (String img : s.keySet()) {
                    images.put(img, s.get(img));
                }
            } else if (obj.getClass() == SplitSlideBar.class) {
                for (SplitBox split : ((SplitSlideBar) obj).getEnfants()) {
                    Map<String, String> s = sauvegarderImage(split.getContenu());
                    for (String img : s.keySet()) {
                        images.put(img, s.get(img));
                    }
                }
            } else if (obj.getClass() == BUTTON.class) {
                String[] res = ((BUTTON) obj).saveImage();
                if (Objects.nonNull(res)) {
                    images.put(res[0], res[1]);
                }
            } else if (obj.getClass() == IMAGE.class) {
                String[] res = ((IMAGE) obj).saveImage();
                images.put(res[0], res[1]);
            }
        }
        return images;
    }
    public String save(int deep) {
        StringBuilder sauvegarde = new StringBuilder(deep + ":BUTTON:");
        sauvegarde.append(getName()).append("|");
        sauvegarde.append(getMarginX()).append("|");
        sauvegarde.append(getMarginY()).append("|");
        sauvegarde.append(getSizeX()).append("|");
        sauvegarde.append(getSizeY()).append("|");
        sauvegarde.append(getPaddingX()).append("|");
        sauvegarde.append(getPaddingY()).append("|");
        sauvegarde.append(getBackgroundColor().getRed()).append("|");
        sauvegarde.append(getBackgroundColor().getGreen()).append("|");
        sauvegarde.append(getBackgroundColor().getBlue()).append("|");
        sauvegarde.append(getForegroundColor().getRed()).append("|");
        sauvegarde.append(getForegroundColor().getGreen()).append("|");
        sauvegarde.append(getForegroundColor().getBlue()).append("|");
        sauvegarde.append(getMyFont().getName()).append("|");
        sauvegarde.append(getMyFont().getSize()).append("|");
        sauvegarde.append(getMyFont().getStyle()).append("|");
        sauvegarde.append(getText()).append("|");
        sauvegarde.append(isCenterX()).append("|");
        sauvegarde.append(isCenterY()).append("|");
        sauvegarde.append(isReductible()).append("|");
        sauvegarde.append(getAction()).append("|");
        if (getActionneur().getClass() == ContainerBox.class) {
            sauvegarde.append(((ContainerBox) getActionneur()).getName()).append("|");
        } else if (getActionneur().getClass() == SplitSlideBar.class) {
            sauvegarde.append(((SplitSlideBar) getActionneur()).getName()).append("|");
        } else if (getActionneur().getClass() == FloatingBox.class) {
            sauvegarde.append(((FloatingBox) getActionneur()).getContenu().getName()).append("|");
        } else if (getActionneur().getClass() == BUTTON.class) {
            sauvegarde.append(((BUTTON) getActionneur()).getName()).append("|");
        }
        sauvegarde.append("<");
        for (Object p : getParametersAction()) {
            if (p.getClass() == ContainerBox.class) {
                sauvegarde.append(((ContainerBox) p).getName()).append("|");
            } else if (p.getClass() == SplitSlideBar.class) {
                sauvegarde.append(((SplitSlideBar) p).getName()).append("|");
            } else if (p.getClass() == FloatingBox.class) {
                sauvegarde.append(((FloatingBox) p).getContenu().getName()).append("|");
            } else {
                sauvegarde.append(p).append("|");
            }
        }
        sauvegarde.append(">|");
        return sauvegarde.toString();
    }
    public String[] saveImage() {
        StringBuilder code = new StringBuilder();
        if (getText().contains("\\")) {
            BufferedImage img = (BufferedImage) getImage();
            code.append(getText().split("\\\\")[getText().split("\\\\").length-1].split("\\.")[1]);
            code.append("|").append(img.getWidth()).append("|").append(img.getHeight()).append("|");
            int lastRGB = img.getRGB(0, 0);
            int nbIter = 0;
            for (int x = 0; x < img.getWidth(); x++) {
                for (int y = 0; y < img.getHeight(); y++) {
                    if (img.getRGB(x, y) == lastRGB) {
                        nbIter++;
                    } else {
                        code.append(nbIter).append("x").append(lastRGB).append("|");
                        lastRGB = img.getRGB(x, y);
                        nbIter = 1;
                    }
                }
            }
            code.append(nbIter).append("x").append(lastRGB).append("|");
            return new String[] {getText().split("\\\\")[getText().split("\\\\").length-1], code.toString()};
        }
        return null;
    }


    public void setName(String name) {
        this.name = name;
    }
    public void setMarginX(int marginX) {
        this.marginX = marginX;
    }
    public void setMarginY(int marginY) {
        this.marginY = marginY;
    }
    public void setSizeX(int sizeX) {
        this.sizeX = sizeX;
    }
    public void setSizeY(int sizeY) {
        this.sizeY = sizeY;
    }
    public void setPaddingX(int paddingX) {
        this.paddingX = paddingX;
    }
    public void setPaddingY(int paddingY) {
        this.paddingY = paddingY;
    }
    public void setBackgroundColor(Color color) {
        backgroundColor = color;
    }
    public void setForegroundColor(Color color) {
        foregroundColor = color;
    }
    public void setMyFont(Font font) {
        myFont = font;
    }
    public void setFontSize(int size) {
        myFont = new Font(myFont.getFontName(), myFont.getStyle(), size);
    }
    public void setFontName(String name) {
        myFont = new Font(name, myFont.getStyle(), myFont.getSize());
    }
    public void setFontStyle(int style) {
        myFont = new Font(myFont.getFontName(), style, myFont.getSize());
    }
    public void setText(String Text) {
        this.Text = Text;
    }
    public void setImage() {
        myImage = loadImage(getText());
    }
    public void setCenterX(boolean centerX) {
        this.centerX = centerX;
    }
    public void setCenterY(boolean centerY) {
        this.centerY = centerY;
    }
    public void setReductible(boolean reductible) {
        this.reductible = reductible;
    }
    public void setCommand(Object actionneur, int action, Object... parametres) {
        this.actionneur = actionneur;
        this.action = action;
        this.parametersAction = parametres;
    }

    public String getName() {
        return name;
    }
    public int getPosX() {
        if (getMarginX() >= 0) {
            return parent.getPosX() + getMarginX();
        } else {
            return parent.getPosX() + ((parent.getSizeX() - getSizeX()) / 2);
        }
    }
    public int getPosY() {
        if (getMarginY() >= 0) {
            return parent.getPosY() + getMarginY();
        } else {
            return parent.getPosY() + ((parent.getSizeY() - getSizeY()) / 2);
        }
    }
    public int getMarginX() {
        return marginX;
    }
    public int getMarginY() {
        return marginY;
    }
    public int getSizeX() {
        return sizeX;
    }
    public int getSizeY() {
        return sizeY;
    }
    public int getPaddingX() {
        return paddingX;
    }
    public int getPaddingY() {
        return paddingY;
    }
    public Color getBackgroundColor() {
        return backgroundColor;
    }
    public Color getForegroundColor() {
        return foregroundColor;
    }
    public Font getMyFont() {
        return myFont;
    }
    public String getText() {
        return Text;
    }
    public Image getImage() {
        return myImage;
    }
    public boolean isCenterX() {
        return centerX;
    }
    public boolean isCenterY() {
        return centerY;
    }
    public boolean isReductible() {
        return reductible;
    }
    public Object getActionneur() {
        return actionneur;
    }
    public int getAction() {
        return action;
    }
    public Object[] getParametersAction() {
        return parametersAction;
    }
}
