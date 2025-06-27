package composants;

import java.awt.*;
import java.util.ArrayList;
import java.util.Objects;

public class ContainerBox {

    String name;
    Parametres mySettings;
    Object parent;
    ArrayList<Object> contenu = new ArrayList<>();
    int marginX;
    int marginY;
    int sizeX;
    int sizeY;
    int row = 0;
    int column = 2;
    int child = 0;
    Color backgroundColor = Color.lightGray;
    SlideBar slider = new SlideBar(this, null);

    public ContainerBox(String name, Parametres settings, Object parent, int... parametres) {
        setName(name);
        mySettings = settings;
        getSlider().setSettings(mySettings);
        this.parent = parent;
        if (parametres.length != 0) {
            setMarginX(parametres[0]);
            setMarginY(parametres[1]);
            setSizeX(parametres[2]);
            setSizeY(parametres[3]);
        }
    }

    public void draw(Graphics g) {
        int pX = (int) (getPosX() * mySettings.rapportX);
        int pY = (int) (getPosY() * mySettings.rapportY);
        int sX = (int) (getSizeX() * mySettings.rapportX);
        int sY = (int) (getSizeY() * mySettings.rapportY);

        g.setColor(getBackgroundColor());
        g.fillRect(pX, pY, sX, sY);
        g.setColor(Color.black);
        g.drawRect(pX, pY, sX, sY);

        for (Object objet : getContenu()) {
            if (objet.getClass() == TEXTZONE.class) {
                TEXTZONE newObj = (TEXTZONE) objet;
                newObj.draw(g);
            } else if (objet.getClass() == TEXT.class) {
                TEXT newObj = (TEXT) objet;
                newObj.draw(g);
            } else if (objet.getClass() == IMAGE.class) {
                IMAGE newObj = (IMAGE) objet;
                newObj.draw(g);
            } else if (objet.getClass() == BUTTON.class) {
                BUTTON newObj = (BUTTON) objet;
                newObj.draw(g);
            } else if (objet.getClass() == ContainerBox.class) {
                ContainerBox newObj = (ContainerBox) objet;
                newObj.draw(g);
            } else if (objet.getClass() == FloatingBox.class) {
                FloatingBox newObj = (FloatingBox) objet;
                newObj.draw(g);
            } else if (objet.getClass() == SplitSlideBar.class) {
                SplitSlideBar newObj = (SplitSlideBar) objet;
                newObj.draw(g);
            }
        }

        if (getChild().length != 0) {
            if (getSlider().isSens()) {
                int nbRow = getRow();
                getSlider().setTotal((int) (nbRow * (getChild()[0].getSizeY() * mySettings.rapportY + getChild()[0].getMarginY() * mySettings.rapportY) + getChild()[0].getMarginY() * mySettings.rapportY));
            } else {
                int nbColumn = getColumn();
                getSlider().setTotal((int) (nbColumn * (getChild()[0].getSizeX() * mySettings.rapportX + getChild()[0].getMarginX() * mySettings.rapportX) + getChild()[0].getMarginX() * mySettings.rapportX));
            }
        } else {
            getSlider().setTotal(0);
        }
        getSlider().drawSlideBar(g);
    }
    public void addObject(String nom, String obj, int... parametres) {
        if (Objects.equals(obj, "TEXTZONE")) {
            TEXTZONE newObj = new TEXTZONE(nom, mySettings, this, parametres);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "TEXT")) {
            TEXT newObj = new TEXT(nom, mySettings, this, parametres);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "BUTTON")) {
            BUTTON newObj = new BUTTON(nom, mySettings, this, parametres);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "ContainerBox")) {
            ContainerBox newObj = new ContainerBox(nom, mySettings, this, parametres);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "SplitSlideBar")) {
            SplitSlideBar newObj = new SplitSlideBar(nom, mySettings, this, parametres);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "FloatingBox")) {
            FloatingBox newObj = new FloatingBox(nom, mySettings, this, parametres);
            getContenu().add(newObj);
            child++;
        }
    }
    public void addObject(String nom, String obj, String textInit, int... parametres) {
        if (Objects.equals(obj, "TEXTZONE")) {
            TEXTZONE newObj = new TEXTZONE(nom, mySettings, this, parametres);
            newObj.setText(textInit);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "TEXT")) {
            TEXT newObj = new TEXT(nom, mySettings, this, parametres);
            newObj.setText(textInit);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "BUTTON")) {
            BUTTON newObj = new BUTTON(nom, mySettings, this, textInit, parametres);
            getContenu().add(newObj);
        } else if (Objects.equals(obj, "IMAGE")) {
            IMAGE newObj = new IMAGE(nom, mySettings, this, textInit, parametres);
            getContenu().add(newObj);
        }
    }
    public void removeObject(String nom) {
        for (Object obj : getContenu()) {
            if (obj.getClass() == TEXT.class) {
                if (Objects.equals(((TEXT) obj).getName(), nom)) {
                    getContenu().remove(obj);
                }
            } else if (obj.getClass() == TEXTZONE.class) {
                if (Objects.equals(((TEXTZONE) obj).getName(), nom)) {
                    getContenu().remove(obj);
                }
            } else if (obj.getClass() == IMAGE.class) {
                if (Objects.equals(((IMAGE) obj).getName(), nom)) {
                    getContenu().remove(obj);
                }
            } else if (obj.getClass() == BUTTON.class) {
                if (Objects.equals(((BUTTON) obj).getName(), nom)) {
                    getContenu().remove(obj);
                }
            } else if (obj.getClass() == SplitSlideBar.class) {
                if (Objects.equals(((SplitSlideBar) obj).getName(), nom)) {
                    getContenu().remove(obj);
                } else {
                    if (Objects.equals(((SplitSlideBar) obj).getContenu().getName(), nom)) {
                        getContenu().remove(((SplitSlideBar) obj).getContenu());
                    } else {
                        ((SplitSlideBar) obj).getContenu().removeObject(nom);
                    }
                }
            } else if (obj.getClass() == FloatingBox.class) {
                if (Objects.equals(((FloatingBox) obj).getContenu().getName(), nom)) {
                    getContenu().remove(obj);
                } else {
                    ((FloatingBox) obj).getContenu().removeObject(nom);
                }
            } else if (obj.getClass() == ContainerBox.class) {
                if (Objects.equals(((ContainerBox) obj).getName(), nom)) {
                    getContenu().remove(obj);
                } else {
                    ((ContainerBox) obj).removeObject(nom);
                }
            }
        }
    }
    public Object getObject(int... index) {
        ContainerBox me = this;

        if (index.length == 0) {
            return me;
        } else if (index.length == 1) {
            return me.getContenu().get(index[0]);
        } else {
            if (me.getContenu().get(index[0]).getClass() == ContainerBox.class) {
                int[] newIndex = new int[index.length - 1];
                System.arraycopy(index, 1, newIndex, 0, newIndex.length);
                return ((ContainerBox) me.getContenu().get(index[0])).getObject(newIndex);
            } else if (me.getContenu().get(index[0]).getClass() == FloatingBox.class) {
                int[] newIndex = new int[index.length - 1];
                System.arraycopy(index, 1, newIndex, 0, newIndex.length);
                return ((FloatingBox) me.getContenu().get(index[0])).getObject(newIndex);
            }  else if (me.getContenu().get(index[0]).getClass() == SplitBox.class) {
                int[] newIndex = new int[index.length - 1];
                System.arraycopy(index, 1, newIndex, 0, newIndex.length);
                return ((SplitBox) me.getContenu().get(index[0])).getObject(newIndex);
            } else {
                return me.getContenu().get(index[0]);
            }
        }
    }
    public Object getObject(String nom) {
        if (Objects.equals(nom, getName())) {
            return this;
        }
        for (Object obj : getContenu()) {
            if (obj.getClass() == TEXT.class) {
                if (Objects.equals(((TEXT) obj).getName(), nom)) {
                    return obj;
                }
            } else if (obj.getClass() == TEXTZONE.class) {
                if (Objects.equals(((TEXTZONE) obj).getName(), nom)) {
                    return obj;
                }
            } else if (obj.getClass() == IMAGE.class) {
                if (Objects.equals(((IMAGE) obj).getName(), nom)) {
                    return obj;
                }
            } else if (obj.getClass() == BUTTON.class) {
                if (Objects.equals(((BUTTON) obj).getName(), nom)) {
                    return obj;
                }
            } else if (obj.getClass() == SplitSlideBar.class) {
                if (Objects.equals(((SplitSlideBar) obj).getName(), nom)) {
                    return obj;
                } else {
                    if (Objects.equals(((SplitSlideBar) obj).getContenu().getName(), nom)) {
                        return ((SplitSlideBar) obj).getContenu();
                    } else {
                        for (SplitBox c : ((SplitSlideBar) obj).getEnfants()) {
                            Object res = c.getContenu().getObject(nom);
                            if (Objects.nonNull(res)) {
                                return res;
                            }
                        }
                    }
                }
            } else if (obj.getClass() == FloatingBox.class) {
                if (Objects.equals(((FloatingBox) obj).getContenu().getName(), nom)) {
                    return ((FloatingBox) obj).getContenu();
                } else {
                    Object res = ((FloatingBox) obj).getContenu().getObject(nom);
                    if (Objects.nonNull(res)) {
                        return res;
                    }
                }
            } else if (obj.getClass() == ContainerBox.class) {
                if (Objects.equals(((ContainerBox) obj).getName(), nom)) {
                    return obj;
                } else {
                    Object res = ((ContainerBox) obj).getObject(nom);
                    if (Objects.nonNull(res)) {
                        return res;
                    }
                }
            }
        }
        return null;
    }
    public void swapChild(String nom1, String nom2) {
        int e1 = 0;
        int e2 = 0;
        for (int i = 0; i < getChild().length; i++) {
            if (Objects.equals(getChild()[i].getContenu().getName(), nom1)) {
                e1 = i;
            }
            if (Objects.equals(getChild()[i].getContenu().getName(), nom2)) {
                e2 = i;
            }
        }
        FloatingBox child1 = getChild()[e1];
        getContenu().set(e1, getChild()[e2]);
        getContenu().set(e2, child1);
    }
    public void swapChild(int i1, int i2) {
        FloatingBox child1 = getChild()[i1];
        FloatingBox child2 = getChild()[i2];
        int index1 = 0;
        int index2 = 0;
        for (int i = 0; i < getContenu().size(); i++) {
            if (Objects.equals(getContenu().get(i), child1)) {
                index1 = i;
            }
            if (Objects.equals(getContenu().get(i), child2)) {
                index2 = i;
            }
        }
        getContenu().set(index1, child2);
        getContenu().set(index2, child1);
    }
    public String save(int deep) {
        StringBuilder sauvegarde = new StringBuilder(deep + ":ContainerBox:");
        sauvegarde.append(getName()).append("|");
        sauvegarde.append(getMarginX()).append("|");
        sauvegarde.append(getMarginY()).append("|");
        sauvegarde.append(getSizeX()).append("|");
        sauvegarde.append(getSizeY()).append("|");
        sauvegarde.append(getRow()).append("|");
        sauvegarde.append(getColumn()).append("|");
        sauvegarde.append(getNbChild()).append("|");
        sauvegarde.append(getBackgroundColor().getRed()).append("|");
        sauvegarde.append(getBackgroundColor().getGreen()).append("|");
        sauvegarde.append(getBackgroundColor().getBlue()).append("|");
        sauvegarde.append(getSlider().getBackgroundColor().getRed()).append("|");
        sauvegarde.append(getSlider().getBackgroundColor().getGreen()).append("|");
        sauvegarde.append(getSlider().getBackgroundColor().getBlue()).append("|");
        sauvegarde.append(getSlider().getForegroundColor().getRed()).append("|");
        sauvegarde.append(getSlider().getForegroundColor().getGreen()).append("|");
        sauvegarde.append(getSlider().getForegroundColor().getBlue()).append("|");
        sauvegarde.append(getSlider().getSize()).append("|");
        sauvegarde.append(getSlider().isSens()).append("|");
        sauvegarde.append(getSlider().isVisible()).append("|");
        return sauvegarde.toString();
    }
    public void resetContenu(ArrayList<Object> contenu) {
        this.contenu = contenu;
    }

    public void setSettings(Parametres settings) {
        mySettings = settings;
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
    public void setRow(int row) {
        this.row = row;
    }
    public void setColumn(int column) {
        this.column = column;
    }
    public void setBackgroundColor(Color color) {
        backgroundColor = color;
    }
    public void setSliderSens(boolean sens) {
        getSlider().setSens(sens);
    }
    public void setSliderVisible(boolean visible) {
        getSlider().setVisible(visible);
    }
    public void setSliderPourcent(float pourcent) {
        getSlider().setPourcent(pourcent);
    }
    public void setSliderBackgroundColor(Color color) {
        getSlider().setBackgroundColor(color);
    }
    public void setSliderForegroundColor(Color color) {
        getSlider().setForegroundColor(color);
    }

    public String getName() {
        return name;
    }
    public Object getParent() {
        return parent;
    }
    public ArrayList<Object> getContenu() {
        return contenu;
    }
    public FloatingBox[] getChild() {
        FloatingBox[] allChilds = new FloatingBox[getNbChild()];
        int index = 0;
        for (Object obj : getContenu()) {
            if (obj.getClass() == FloatingBox.class) {
                allChilds[index] = (FloatingBox) obj;
                index++;
            }
        }
        return allChilds;
    }
    public int getPosX() {
        int add = 0;
        int size = 0;
        if (Objects.nonNull(parent)) {
            if (parent.getClass() == ContainerBox.class) {
                add = ((ContainerBox) parent).getPosX();
                size = ((ContainerBox) parent).getSizeX();
            } else if (parent.getClass() == FloatingBox.class) {
                add = ((FloatingBox) parent).getPosX();
                size = ((FloatingBox) parent).getSizeX();
            } else if (parent.getClass() == SplitBox.class) {
                add = ((SplitBox) parent).getPosX();
                size = ((SplitBox) parent).getSizeX();
            }
        }
        if (getMarginX() >= 0) {
            return add + getMarginX();
        } else {
            return add + ((size - getSizeX()) / 2);
        }
    }
    public int getPosY() {
        int add = 0;
        int size = 0;
        if (Objects.nonNull(parent)) {
            if (parent.getClass() == ContainerBox.class) {
                add = ((ContainerBox) parent).getPosY();
                size = ((ContainerBox) parent).getSizeY();
            } else if (parent.getClass() == FloatingBox.class) {
                add = ((FloatingBox) parent).getPosY();
                size = ((FloatingBox) parent).getSizeY();
            } else if (parent.getClass() == SplitBox.class) {
                add = ((SplitBox) parent).getPosY();
                size = ((SplitBox) parent).getSizeY();
            }
        }
        if (getMarginY() >= 0) {
            return add + getMarginY();
        } else {
            return add + ((size - getSizeY()) / 2);
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
    public int getRow() {
        if (getSlider().isSens()) {
            int nbChild = getChild().length;
            int total = nbChild / column;
            if ((float) nbChild / column - total > 0) {
                total += 1;
            }
            return total;
        }
        return row;
    }
    public int getColumn() {
        if (!getSlider().isSens()) {
            int nbChild = getChild().length;
            int total = nbChild / row;
            if ((float) nbChild / row - total > 0) {
                total += 1;
            }
            return total;
        }
        return column;
    }
    public int getNbChild() {
        return child;
    }
    public Color getBackgroundColor() {
        return backgroundColor;
    }
    public SlideBar getSlider() {
        return slider;
    }
    public Parametres getSettings() {
        return mySettings;
    }
}
