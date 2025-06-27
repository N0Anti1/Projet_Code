package composants;

import java.awt.*;
import java.util.ArrayList;
import java.util.Objects;

public class TEXTZONE {

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
    Color foregroundColorWaiting = Color.gray;
    Font myFont;
    String Text = "";
    String textWaiting = "Entrez du texte";
    SlideBar slider = new SlideBar(this, null);
    boolean center = false;
    boolean newLine = true;

    public TEXTZONE(String name, Parametres settings, ContainerBox parent, int... parametres) {
        setName(name);
        mySettings = settings;
        getSlider().setSettings(mySettings);
        getSlider().setPourcent(100);
        setMyFont(mySettings.mainTheme.mainFont);
        this.parent = parent;
        if (parametres.length != 0) {
            setMarginX(parametres[0]);
            setMarginY(parametres[1]);
            setSizeX(parametres[2]);
            setSizeY(parametres[3]);
            if (parametres.length == 5) {
                setCenter(parametres[4] == -1);
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

        setFontSize((int) (mySettings.mainTheme.mainFont.getSize() * mySettings.rapportM));
        g.setFont(getMyFont());
        g.setColor(getBackgroundColor());
        g.fillRect(pX, pY, sX, sY);
        g.setColor(Color.black);
        g.drawRect(pX, pY, sX, sY);
        g.setColor(getForegroundColor());
        FontMetrics metrics = g.getFontMetrics(g.getFont());

        String message = getText();
        if (message.toCharArray().length == 0) {
            message = getTextWaiting();
            g.setColor(getForegroundColorWaiting());
        }
        ArrayList<String> texts = splitText(message, metrics);

        int indexLine = 0;
        for (String line : texts) {
            if (mY + metrics.getHeight() * indexLine + metrics.getHeight() / 1.5 - getSlider().getDepassement() < sY && mY + metrics.getHeight()*indexLine - getSlider().getDepassement() >= 0) {
                int addX = 0;
                if (isCenter()) {
                    addX = (sX - metrics.stringWidth(line)) / 2;
                }
                g.drawString(line, pX + mX + addX, (int) (pY + mY + metrics.getHeight() / 1.5 + metrics.getHeight() * indexLine - getSlider().getDepassement()));
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

    public void addLetter(char lettre, int index) {
        if (getText().length() == index) {
            Text += lettre;
        } else {
            StringBuilder message = new StringBuilder();
            char[] actuelText = getText().toCharArray();
            for (int i = 0; i < actuelText.length; i++) {
                if (i == index) {
                    message.append(lettre);
                }
                message.append(actuelText[i]);
            }
            Text = message.toString();
        }
    }
    public void removeLetter(int index) {
        StringBuilder message = new StringBuilder();
        char[] actuelText = getText().toCharArray();
        for (int i = 0; i < actuelText.length; i++) {
            if (i != index) {
                message.append(actuelText[i]);
            }
        }
        Text = message.toString();
    }
    public String save(int deep) {
        return deep + ":TEXTZONE:" + getName() + "|" +
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
                getForegroundColorWaiting().getRed() + "|" +
                getForegroundColorWaiting().getGreen() + "|" +
                getForegroundColorWaiting().getBlue() + "|" +
                getMyFont().getName() + "|" +
                getMyFont().getSize() + "|" +
                getMyFont().getStyle() + "|" +
                getText().replace("\n", "\\n") + "|" +
                getTextWaiting().replace("\n", "\\n") + "|" +
                getSlider().getBackgroundColor().getRed() + "|" +
                getSlider().getBackgroundColor().getGreen() + "|" +
                getSlider().getBackgroundColor().getBlue() + "|" +
                getSlider().getForegroundColor().getRed() + "|" +
                getSlider().getForegroundColor().getGreen() + "|" +
                getSlider().getForegroundColor().getBlue() + "|" +
                getSlider().getSize() + "|" +
                getSlider().isSens() + "|" +
                getSlider().isVisible() + "|" +
                isCenter() + "|" +
                isNewLine() + "|";
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
    public void setForegroundColorWaiting(Color color) {
        foregroundColorWaiting = color;
    }
    public void setMyFont(Font font) {
        myFont = font;
    }
    public void setText(String Text) {
        this.Text = Text;
    }
    public void setTextWaiting(String textWaiting) {
        this.textWaiting = textWaiting;
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
    public void setCenter(boolean center) {
        this.center = center;
    }
    public void setNewLine(boolean newLine) {
        this.newLine = newLine;
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
    public Color getForegroundColorWaiting() {
        return foregroundColorWaiting;
    }
    public Font getMyFont() {
        return myFont;
    }
    public String getText() {
        return Text;
    }
    public String getTextWaiting() {
        return textWaiting;
    }
    public SlideBar getSlider() {
        return slider;
    }
    public boolean isCenter() {
        return center;
    }
    public boolean isNewLine() {
        return newLine;
    }
}
