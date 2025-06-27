package composants;

import java.awt.*;
import java.util.ArrayList;
import java.util.Objects;

public class TEXT {

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
    SlideBar slider = new SlideBar(this, null);
    boolean centerX = false;
    boolean centerY = false;
    boolean reductible = false;

    public TEXT(String name, Parametres settings, ContainerBox parent, int... parametres) {
        setName(name);
        mySettings = settings;
        getSlider().setSettings(mySettings);
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

    public void draw(Graphics g) {
        int pX = (int) (getPosX() * mySettings.rapportX);
        int pY = (int) (getPosY() * mySettings.rapportY);
        int sX = (int) (getSizeX() * mySettings.rapportX);
        int sY = (int) (getSizeY() * mySettings.rapportY);
        int mX = (int) (getPaddingX() * mySettings.rapportX);
        int mY = (int) (getPaddingY() * mySettings.rapportY);
        if (isCenterY()) {
            mY = 0;
        }
        if (isCenterX()) {
            mX = 0;
        }

        g.setColor(getBackgroundColor());
        g.fillRect(pX, pY, sX, sY);
        g.setColor(Color.black);
        g.drawRect(pX, pY, sX, sY);

        g.setColor(getForegroundColor());
        setFontSize((int) (mySettings.mainTheme.mainFont.getSize() * mySettings.rapportM));
        g.setFont(getMyFont());
        FontMetrics metrics = g.getFontMetrics(g.getFont());

        if (isReductible()) {
            while (splitText(getText(), metrics).size() * metrics.getHeight() + mY >= sY) {
                setFontSize(getMyFont().getSize()-1);
                g.setFont(getMyFont());
                metrics = g.getFontMetrics(g.getFont());
            }
        }
        ArrayList<String> texts = splitText(getText(), metrics);

        int indexLine = 0;
        for (String line : texts) {
            if (mY + metrics.getHeight() * indexLine + metrics.getHeight() / 1.5 - getSlider().getDepassement() < sY && mY + metrics.getHeight()*indexLine - getSlider().getDepassement() >= 0) {
                int addX = 0;
                int addY = 0;
                if (isCenterX()) {
                    addX = (sX - metrics.stringWidth(line)) / 2;
                }
                if (isCenterY()) {
                    if (mY + metrics.getHeight() * texts.size() < sY) {
                        addY = (sY - (mY + metrics.getHeight()) * texts.size()) / 2;
                    }
                }
                g.drawString(line, pX + mX + addX, (int) (pY + mY + addY + metrics.getHeight() / 1.5 + metrics.getHeight() * indexLine - getSlider().getDepassement()));
            }
            indexLine++;
        }
        getSlider().setTotal(mY + metrics.getHeight() * texts.size());
        getSlider().drawSlideBar(g);
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
    public String save(int deep) {
        return deep + ":TEXT:" + getName() + "|" +
                getMarginX() + "|" +
                getMarginY() + "|" +
                getSizeX() + "|" +
                getSizeY() + "|" +
                getPaddingX() + "|" +
                getPaddingY() + "|" +
                getBackgroundColor().getRed() + "|" +
                getBackgroundColor().getGreen() + "|" +
                getBackgroundColor().getBlue() + "|" +
                getForegroundColor().getRed() + "|" +
                getForegroundColor().getGreen() + "|" +
                getForegroundColor().getBlue() + "|" +
                getMyFont().getName() + "|" +
                getMyFont().getSize() + "|" +
                getMyFont().getStyle() + "|" +
                getText().replace("\n", "\\n") + "|" +
                getSlider().getBackgroundColor().getRed() + "|" +
                getSlider().getBackgroundColor().getGreen() + "|" +
                getSlider().getBackgroundColor().getBlue() + "|" +
                getSlider().getForegroundColor().getRed() + "|" +
                getSlider().getForegroundColor().getGreen() + "|" +
                getSlider().getForegroundColor().getBlue() + "|" +
                getSlider().getSize() + "|" +
                getSlider().isSens() + "|" +
                getSlider().isVisible() + "|" +
                isCenterX() + "|" +
                isCenterY() + "|" +
                isReductible() + "|";
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
    public void setText(String Text) {
        this.Text = Text;
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
    public void setCenterX(boolean centerX) {
        this.centerX = centerX;
    }
    public void setCenterY(boolean centerY) {
        this.centerY = centerY;
    }
    public void setReductible(boolean reductible) {
        this.reductible = reductible;
    }

    public String getName() {
        return name;
    }
    public ContainerBox getParent() {
        return parent;
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
    public SlideBar getSlider() {
        return slider;
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
}
