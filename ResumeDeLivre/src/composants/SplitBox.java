package composants;

import java.awt.*;

public class SplitBox {

    Parametres mySettings;
    SplitSlideBar parent;
    int PersonalIndex;
    ContainerBox contenu;

    public SplitBox(String name, Parametres settings, SplitSlideBar parent, int index) {
        mySettings = settings;
        this.parent = parent;
        setIndex(index);
        contenu = new ContainerBox(name, mySettings, this, 0, 0, getSizeX(), getSizeY());
    }

    public void draw(Graphics g) {
        getContenu().draw(g);
    }
    public Object getObject(int... index) {
        SplitBox me = this;

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
        StringBuilder sauvegarde = new StringBuilder(deep + ":SplitBox:");
        sauvegarde.append(getContenu().getName()).append("|");
        sauvegarde.append(getIndex()).append("|");
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

    public void setIndex(int index) {
        PersonalIndex = index;
    }

    public SplitSlideBar getParent() {
        return parent;
    }
    public int getIndex() {
        return PersonalIndex;
    }
    public int getPosX() {
        return parent.getPosX();
    }
    public int getPosY() {
        return parent.getPosY();
    }
    public int getSizeX() {
        return parent.getSizeX();
    }
    public int getSizeY() {
        return parent.getSizeY();
    }
    public ContainerBox getContenu() {
        return contenu;
    }
}
