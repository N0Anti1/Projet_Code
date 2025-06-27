package composants;

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Objects;

public class SplitSlideBar {

    String name;
    Parametres mySettings;
    ContainerBox parent;
    ArrayList<SplitBox> enfants = new ArrayList<>();
    int marginX;
    int marginY;
    int sizeX;
    int sizeY;
    int width = 20;
    Color backgroundColor = new Color(230, 230, 230);
    Color foregroundColor = new Color(150, 150, 150);
    Color cursorColor = new Color(255, 255, 255);
    int depassement = 0;

    public SplitSlideBar(String name, Parametres settings, ContainerBox parent, int... parametres) {
        setName(name);
        mySettings = settings;
        this.parent = parent;
        if (parametres.length != 0) {
            setMarginX(parametres[0]);
            setMarginY(parametres[1]);
            setSizeX(parametres[2]);
            setSizeY(parametres[3]);
        }
    }
    public void draw(Graphics g) {
        getEnfants().get(getIndexContent()).draw(g);
        drawSplitSlide(g);
    }
    public void drawSplitSlide(Graphics g) {
        int pX = (int) (getPosX() * mySettings.rapportX);
        int pY = (int) (getPosY() * mySettings.rapportY);
        int sX = (int) (getSizeX() * mySettings.rapportX);
        int sY = (int) (getSizeY() * mySettings.rapportY);
        int w = (int) (getWidth() * mySettings.rapportY);

        g.setColor(getBackgroundColor());
        g.fillRect(pX, pY + sY, sX, w);
        g.setColor(Color.black);
        g.drawRect(pX, pY + sY, sX, w);

        int[] xPos = new int[getEnfants().size()];
        if (getEnfants().size() > 1) {
            for (int i = 0; i < getEnfants().size(); i++) {
                xPos[i] = ((sX + 1) * i / getEnfants().size()) + ((sX + 1) / (2 * getEnfants().size()));
            }
        } else {
            Arrays.fill(xPos, 0);
        }
        g.setColor(getForegroundColor());
        for (int xPo : xPos) {
            int p = 1;
            if (sX / getEnfants().size() < w) {
                if (sX / getEnfants().size() < w / 2) {
                    p = 4;
                } else {
                    p = 2;
                }
            }
            g.fillRect(pX + xPo - w / (4 * p), pY + sY, w / (2 * p), w);
        }

        g.setColor(getCursorColor());
        g.fillPolygon(new int[] {pX + getDepassement(), pX + getDepassement() + 5, pX + getDepassement() - 5},
                new int[] {pY + sY, pY + sY + w, pY + sY + w}, 3);
        g.setColor(Color.black);
        g.drawPolygon(new int[] {pX + getDepassement(), pX + getDepassement() + 5, pX + getDepassement() - 5},
                new int[] {pY + sY, pY + sY + w, pY + sY + w}, 3);
    }
    public void swapChild(String nom1, String nom2) {
        int e1 = 0;
        int e2 = 0;
        for (int i = 0; i < getEnfants().size(); i++) {
            if (Objects.equals(getEnfant(i).getName(), nom1)) {
                e1 = i;
            }
            if (Objects.equals(getEnfant(i).getName(), nom2)) {
                e2 = i;
            }
        }
        int index1 = getEnfants().get(e1).getIndex();
        SplitBox child1 = getEnfants().get(e1);
        getEnfants().get(e1).setIndex(getEnfants().get(e2).getIndex());
        getEnfants().get(e2).setIndex(index1);
        getEnfants().set(e1, getEnfants().get(e2));
        getEnfants().set(e2, child1);
    }
    public void swapChild(int i1, int i2) {
        int index1 = getEnfants().get(i1).getIndex();
        SplitBox child1 = getEnfants().get(i1);
        getEnfants().get(i1).setIndex(getEnfants().get(i2).getIndex());
        getEnfants().get(i2).setIndex(index1);
        getEnfants().set(i1, getEnfants().get(i2));
        getEnfants().set(i2, child1);
    }
    public String save(int deep) {
        StringBuilder sauvegarde = new StringBuilder(deep + ":SplitSlideBar:");
        sauvegarde.append(getName()).append("|");
        sauvegarde.append(getMarginX()).append("|");
        sauvegarde.append(getMarginY()).append("|");
        sauvegarde.append(getSizeX()).append("|");
        sauvegarde.append(getSizeY()).append("|");
        sauvegarde.append(getWidth()).append("|");
        sauvegarde.append(getBackgroundColor().getRed()).append("|");
        sauvegarde.append(getBackgroundColor().getGreen()).append("|");
        sauvegarde.append(getBackgroundColor().getBlue()).append("|");
        sauvegarde.append(getForegroundColor().getRed()).append("|");
        sauvegarde.append(getForegroundColor().getGreen()).append("|");
        sauvegarde.append(getForegroundColor().getBlue()).append("|");
        sauvegarde.append(getCursorColor().getRed()).append("|");
        sauvegarde.append(getCursorColor().getGreen()).append("|");
        sauvegarde.append(getCursorColor().getBlue()).append("|");
        return sauvegarde.toString();
    }


    public void setName(String name) {
        this.name = name;
    }
    public void addChild(String nom) {
        getEnfants().add(new SplitBox(nom, mySettings, this, getEnfants().size()));
    }
    public void removeChild(SplitBox child) {
        getEnfants().remove(child);
    }
    public void removeChild(int index) {
        getEnfants().remove(index);
    }
    public void removeChild(String nom) {
        for (int i = 0; i < getEnfants().size(); i++) {
            if (Objects.equals(getEnfants().get(i).getContenu().getName(), nom)) {
                removeChild(i);
                break;
            }
        }
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
    public void setWidth(int width) {
        this.width = width;
    }
    public void setSliderBackgroundColor(Color color) {
        backgroundColor = color;
    }
    public void setSliderForegroundColor(Color color) {
        foregroundColor = color;
    }
    public void setCursorColor(Color color) {
        cursorColor = color;
    }
    public void setIndexContent(int index) {
        if (getEnfants().size() > 1) {
            depassement = (int) (((getSizeX() + 1) * index * mySettings.rapportX / getEnfants().size()) + ((getSizeX() + 1) * mySettings.rapportX / (2 * getEnfants().size())));
        } else {
            depassement = 0;
        }
    }
    public void addDepassement(int delta) {
        depassement += delta;
        if (depassement < 0) {
            depassement = 0;
        } else if (depassement > getSizeX() * mySettings.rapportX) {
            depassement = (int) (getSizeX() * mySettings.rapportX);
        }
    }
    public void resetDepassement() {
        int index = getIndexContent();
        setIndexContent(index);
    }


    public String getName() {
        return name;
    }
    public ContainerBox getParent() {
        return parent;
    }
    public ArrayList<SplitBox> getEnfants() {
        return enfants;
    }
    public ContainerBox getEnfant(int index) {
        if (enfants.size() > 0) {
            return enfants.get(index).getContenu();
        } else {
            return new ContainerBox("", mySettings, null);
        }
    }
    public ContainerBox getContenu() {
        return getEnfant(getIndexContent());
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
    public int getWidth() {
        return width;
    }
    public Color getBackgroundColor() {
        return backgroundColor;
    }
    public Color getForegroundColor() {
        return foregroundColor;
    }
    public Color getCursorColor() {
        return cursorColor;
    }
    public int getDepassement() {
        return depassement;
    }
    public int getIndexContent() {
        return (int) (getEnfants().size() * getDepassement() / ((getSizeX() + 1) * mySettings.rapportX));
    }
}
