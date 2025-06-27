package composants;

import java.awt.*;

public class SlideBar {
    Object parent;
    Parametres mySettings;
    int size = 10;
    Color backgroundColor = new Color(200, 200, 200);
    Color foregroundColor = new Color(255, 255, 255);
    boolean visible = true;
    float pourcent = 0.0f;
    int depassement = 0;
    int total = 0;
    boolean sens = true;

    public SlideBar(TEXTZONE heritier, Parametres settings) {
        parent = heritier;
        mySettings = settings;
    }
    public SlideBar(TEXT heritier, Parametres settings) {
        parent = heritier;
        mySettings = settings;
    }
    public SlideBar(ContainerBox heritier, Parametres settings) {
        parent = heritier;
        mySettings = settings;
    }

    public void drawSlideBar(Graphics g) {
        float rapX = mySettings.rapportX;
        float rapY = mySettings.rapportY;
        int x = 0;
        int y = 0;
        int sizeX = 0;
        int sizeY = 0;
        if (parent.getClass() == TEXTZONE.class) {
            TEXTZONE obj = (TEXTZONE) parent;
            if (isSens()) {
                x = (int) (obj.getPosX()*rapX + obj.getSizeX()*rapX - getSize()*rapX);
                y = (int) (obj.getPosY()*rapY);
                sizeX = (int) (getSize()*rapX);
                sizeY = (int) (obj.getSizeY()*rapY);
            } else {
                x = (int) (obj.getPosX()*rapX);
                y = (int) (obj.getPosY()*rapY + obj.getSizeY()*rapY - getSize()*rapY);
                sizeX = (int) (obj.getSizeX()*rapX);
                sizeY = (int) (getSize()*rapY);
            }
        } else if (parent.getClass() == TEXT.class) {
            TEXT obj = (TEXT) parent;
            if (isSens()) {
                x = (int) (obj.getPosX()*rapX + obj.getSizeX()*rapX - getSize()*rapX);
                y = (int) (obj.getPosY()*rapY);
                sizeX = (int) (getSize()*rapX);
                sizeY = (int) (obj.getSizeY()*rapY);
            } else {
                x = (int) (obj.getPosX()*rapX);
                y = (int) (obj.getPosY()*rapY + obj.getSizeY()*rapY - getSize()*rapY);
                sizeX = (int) (obj.getSizeX()*rapX);
                sizeY = (int) (getSize()*rapY);
            }
        } else if (parent.getClass() == ContainerBox.class) {
            ContainerBox obj = (ContainerBox) parent;
            if (isSens()) {
                x = (int) (obj.getPosX()*rapX + obj.getSizeX()*rapX - getSize()*rapX);
                y = (int) (obj.getPosY()*rapY);
                sizeX = (int) (getSize()*rapX);
                sizeY = (int) (obj.getSizeY()*rapY);
            } else {
                x = (int) (obj.getPosX()*rapX);
                y = (int) (obj.getPosY()*rapY + obj.getSizeY()*rapY - getSize()*rapY);
                sizeX = (int) (obj.getSizeX()*rapX);
                sizeY = (int) (getSize()*rapY);
            }
        }

        float largeur = (float) sizeX * sizeX / getTotal();
        float hauteur = (float) sizeY * sizeY / getTotal();
        int newX = (int) (x + (sizeX - largeur) * getPourcent() / 100.);
        int newY = (int) (y + (sizeY - hauteur) * getPourcent() / 100.);
        int taille = sizeY;

        if (isSens()) {
            largeur = sizeX;
            newX = x;
        } else {
            hauteur = sizeY;
            newY = y;
            taille = sizeX;
        }
        if ((float) getTotal() / (float) taille > 1) {
            if (isVisible()) {
                g.setColor(getBackgroundColor());
                g.fillRect(x, y, sizeX, sizeY);
                g.setColor(Color.black);
                g.drawRect(x, y, sizeX, sizeY);
                g.setColor(getForegroundColor());
                g.fillRect(newX, newY, (int) largeur, (int) hauteur);
                g.setColor(Color.black);
                g.drawRect(newX, newY, (int) largeur, (int) hauteur);
            }
            setDepassement((int) ((getTotal() - taille) * getPourcent() / 100));
        } else {
            setDepassement(0);
        }
    }
    public void addPourcent(int p) {
        float rapX = mySettings.rapportX;
        float rapY = mySettings.rapportY;
        int sizeY = 0;
        int sizeX = 0;
        if (parent.getClass() == TEXTZONE.class) {
            TEXTZONE obj = (TEXTZONE) parent;
            sizeY = (int) (obj.getSizeY() * rapY);
            sizeX = (int) (obj.getSizeX() * rapX);
        } else if (parent.getClass() == TEXT.class) {
            TEXT obj = (TEXT) parent;
            sizeY = (int) (obj.getSizeY() * rapY);
            sizeX = (int) (obj.getSizeX() * rapX);
        } else if (parent.getClass() == ContainerBox.class) {
            ContainerBox obj = (ContainerBox) parent;
            sizeY = (int) (obj.getSizeY() * rapY);
            sizeX = (int) (obj.getSizeX() * rapX);
        } else if (parent.getClass() == FloatingBox.class) {
            FloatingBox obj = (FloatingBox) parent;
            sizeY = (int) (obj.getSizeY() * rapY);
            sizeX = (int) (obj.getSizeX() * rapX);
        }
        int size = sizeX;
        if (isSens()) {
            size = sizeY;
        }
        if (getTotal() / (float) size > 1) {
            addDepassement(p);
            setPourcent((float) (100 * getDepassement()) / (getTotal() - size));
            if (getPourcent() < 0) {
                setPourcent(0);
                setDepassement(0);
            } else if (getPourcent() > 100) {
                setPourcent(100);
                setDepassement(getTotal() - size);
            }
        }
    }

    public void setSettings(Parametres settings) {
        mySettings = settings;
    }
    public void setSize(int size) {
        this.size = size;
    }
    public void setBackgroundColor(Color color) {
        backgroundColor = color;
    }
    public void setForegroundColor(Color color) {
        foregroundColor = color;
    }
    public void setVisible(boolean visible) {
        this.visible = visible;
    }
    public void setPourcent(float pourcent) {
        this.pourcent = pourcent;
    }
    public void setDepassement(int depassement) {
        this.depassement = depassement;
    }
    public void addDepassement(int add) {
        depassement += add;
    }
    public void setTotal(int total) {
        this.total = total;
    }
    public void setSens(boolean sens) {
        this.sens = sens;
    }

    public int getSize() {
        return size;
    }
    public Color getBackgroundColor() {
        return backgroundColor;
    }
    public Color getForegroundColor() {
        return foregroundColor;
    }
    public boolean isVisible() {
        return visible;
    }
    public float getPourcent() {
        return pourcent;
    }
    public int getDepassement() {
        return depassement;
    }
    public int getTotal() {
        return total;
    }
    public boolean isSens() {
        return sens;
    }
}
