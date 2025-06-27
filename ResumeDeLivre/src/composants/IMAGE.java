package composants;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.*;
import java.io.File;
import java.io.IOException;
import java.util.Objects;

public class IMAGE {

    String name;
    Parametres mySettings;
    ContainerBox parent;
    String path;
    int marginX;
    int marginY;
    int sizeX;
    int sizeY;
    Color backgroundColor = Color.white;
    BufferedImage myImage;
    Image drawImage;

    float lastRapportX = 0;
    float lastRapportY = 0;
    String lastPath = "";

    public IMAGE(String name, Parametres settings, ContainerBox parent, String path, int... parametres) {
        setName(name);
        mySettings = settings;
        this.parent = parent;
        setPath(path);
        setImage();
        setMarginX(parametres[0]);
        setMarginY(parametres[1]);
        if (parametres.length > 2) {
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
        if (getName().contains("fiche image")) {
            if (!lastPath.equals(mySettings.allPersonnages.get(((TEXT) parent.getObject(1)).getText()).path)) {
                lastPath = mySettings.allPersonnages.get(((TEXT) parent.getObject(1)).getText()).path;
                setPath(lastPath);
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
        g.setColor(Color.black);
        g.drawRect(pX, pY, sX, sY);
    }

    public BufferedImage loadImage(String path) {
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
    public String save(int deep) {
        StringBuilder sauvegarde = new StringBuilder(deep + ":IMAGE:");
        sauvegarde.append(getName()).append("|");
        sauvegarde.append(getPath()).append("|");
        sauvegarde.append(getMarginX()).append("|");
        sauvegarde.append(getMarginY()).append("|");
        sauvegarde.append(getSizeX()).append("|");
        sauvegarde.append(getSizeY()).append("|");
        sauvegarde.append(getBackgroundColor().getRed()).append("|");
        sauvegarde.append(getBackgroundColor().getGreen()).append("|");
        sauvegarde.append(getBackgroundColor().getBlue()).append("|");
        return sauvegarde.toString();
    }
    public String[] saveImage() {
        StringBuilder code = new StringBuilder();
        BufferedImage img = (BufferedImage) getImage();
        code.append(getPath().split("\\\\")[getPath().split("\\\\").length-1].split("\\.")[1]);
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
        return new String[] {getPath().split("\\\\")[getPath().split("\\\\").length-1], code.toString()};
    }

    public void setName(String name) {
        this.name = name;
    }
    public void setPath(String path) {
        this.path = path;
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
    public void setBackgroundColor(Color color) {
        backgroundColor = color;
    }
    public void setImage() {
        myImage = loadImage(getPath());
    }

    public String getName() {
        return name;
    }
    public String getPath() {
        return path;
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
    public Color getBackgroundColor() {
        return backgroundColor;
    }
    public Image getImage() {
        return myImage;
    }
}
