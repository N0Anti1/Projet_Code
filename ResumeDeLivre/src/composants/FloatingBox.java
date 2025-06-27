package composants;

import java.awt.*;
import java.util.ArrayList;
import java.util.Objects;

public class FloatingBox {

    Parametres mySettings;
    ContainerBox parent;
    ContainerBox contenu;
    int marginX;
    int marginY;
    int sizeX;
    int sizeY;

    public FloatingBox(String name, Parametres settings, ContainerBox parent, int... parametres) {
        mySettings = settings;
        this.parent = parent;
        if (parametres.length != 0) {
            setMarginX(parametres[0]);
            setMarginY(parametres[1]);
            setSizeX(parametres[2]);
            setSizeY(parametres[3]);
        }
        setContenu(new ContainerBox(name, mySettings, this, 0, 0, getSizeX(), getSizeY()));
    }
    public void draw(Graphics g) {
        getContenu().draw(g);
    }

    public Object getObject(int... index) {
        FloatingBox me = this;

        if (index.length == 0) {
            return me;
        } else if (index.length == 1) {
            return me.getContenu();
        } else {
            int[] newIndex = new int[index.length - 1];
            System.arraycopy(index, 1, newIndex, 0, newIndex.length);
            return me.getContenu().getObject(newIndex);
        }
    }
    public String save(int deep) {
        StringBuilder sauvegarde = new StringBuilder(deep + ":FloatingBox:");
        sauvegarde.append(getContenu().getName()).append("|");
        sauvegarde.append(getMarginX()).append("|");
        sauvegarde.append(getMarginY()).append("|");
        sauvegarde.append(getSizeX()).append("|");
        sauvegarde.append(getSizeY()).append("|");

        sauvegarde.append(getContenu().getRow()).append("|");
        sauvegarde.append(getContenu().getColumn()).append("|");
        sauvegarde.append(getContenu().getNbChild()).append("|");
        sauvegarde.append(getContenu().getBackgroundColor().getRed()).append("|");
        sauvegarde.append(getContenu().getBackgroundColor().getGreen()).append("|");
        sauvegarde.append(getContenu().getBackgroundColor().getBlue()).append("|");
        sauvegarde.append(getContenu().getSlider().getBackgroundColor().getRed()).append("|");
        sauvegarde.append(getContenu().getSlider().getBackgroundColor().getGreen()).append("|");
        sauvegarde.append(getContenu().getSlider().getBackgroundColor().getBlue()).append("|");
        sauvegarde.append(getContenu().getSlider().getForegroundColor().getRed()).append("|");
        sauvegarde.append(getContenu().getSlider().getForegroundColor().getGreen()).append("|");
        sauvegarde.append(getContenu().getSlider().getForegroundColor().getBlue()).append("|");
        sauvegarde.append(getContenu().getSlider().getSize()).append("|");
        sauvegarde.append(getContenu().getSlider().isSens()).append("|");
        sauvegarde.append(getContenu().getSlider().isVisible()).append("|");
        return sauvegarde.toString();
    }

    public void setContenu(ContainerBox contenu) {
        this.contenu = contenu;
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

    public ContainerBox getContenu() {
        return contenu;
    }
    public int getPosX() {
        FloatingBox[] frere = parent.getChild();
        int Prow = parent.getRow();
        int Pcolumn = parent.getColumn();
        int posX = parent.getPosX() + getMarginX();
        int addX = 0;
        boolean finish = false;

        for (int i = 0; i < Prow; i++) {
            addX = 0;
            for (int j = 0; j < Pcolumn; j++) {
                if (frere[j + i*Pcolumn] == this) {
                    finish = true;
                    break;
                } else {
                    addX += frere[j + i * Pcolumn].getMarginX();
                    addX += frere[j + i * Pcolumn].getSizeX();
                }
            }
            if (finish) {
                break;
            }
        }

        int depassement = 0;
        if (!parent.getSlider().isSens()) {
            depassement = (int) (parent.getSlider().getDepassement() / mySettings.rapportX);
        }

        int pX = parent.getPosX();
        int pSX = parent.getSizeX();
        int x = addX + posX - depassement;
        int sx = getSizeX();

        if (x < pX || x + sx > pX + pSX) {
            return 10000;
        }
        return addX + posX - depassement;
    }
    public int getPosY() {
        FloatingBox[] frere = parent.getChild();
        int Prow = parent.getRow();
        int Pcolumn = parent.getColumn();
        int posY = parent.getPosY() + getMarginY();
        int addY = 0;
        boolean finish = false;

        for (int i = 0; i < Prow; i++) {
            for (int j = 0; j < Pcolumn; j++) {
                if (frere[j + i*Pcolumn] == this) {
                    finish = true;
                    break;
                }
            }
            if (!finish) {
                addY += frere[i * Pcolumn].getMarginY();
                addY += frere[i * Pcolumn].getSizeY();
            } else {
                break;
            }
        }

        int depassement = 0;
        if (parent.getSlider().isSens()) {
            depassement = (int) (parent.getSlider().getDepassement() / mySettings.rapportY);
        }

        int pY = parent.getPosY();
        int pSY = parent.getSizeY();
        int y = addY + posY - depassement;
        int sy = getSizeY();

        if (y < pY || y + sy > pY + pSY) {
            return 10000;
        }
        return addY + posY - depassement;
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
}
