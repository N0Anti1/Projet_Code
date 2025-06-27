package composants;

import javax.swing.text.AttributeSet;
import java.awt.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Parametres {
    public String possibleLetter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 " +
            "&~\"'{}()[]-`_\\^@°=+^¨$£¤%*µ,?;.:/!§<>²ðÐøØ¿¡ß\n" +
            "àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÕÃÑåÅæÆœŒçÇ";
    public float rapportX;
    public float rapportY;
    public float rapportM;
    public String pathImage = "E:\\Dossiers Utilisateurs\\Images";
    public String pathLoad = "C:\\Users\\ERARD\\IdeaProjects\\ResumeDeLivre\\assets\\saves";

    public static class Theme {
        public Color mainColor = new Color(50, 134, 170);
        public Color secondaryColor = new Color(0, 53, 106);
        public Color tertiaryColor = new Color(145, 187, 209);
        public Font mainFont = new Font(Font.SANS_SERIF, Font.PLAIN, 20);
    }
    public Theme mainTheme = new Theme();
    public static class Personnage {
        public String name;
        public String path = "assets\\renard.png";
        public String description = "";
        public Personnage(String name) {
            this.name = name;
        }
    }
    public Map<String, Personnage> allPersonnages = new HashMap<>();

    public String save() {
        StringBuilder sauvegarde = new StringBuilder();
        sauvegarde.append(":Theme:");
        sauvegarde.append(mainTheme.mainColor.getRed()).append("|");
        sauvegarde.append(mainTheme.mainColor.getGreen()).append("|");
        sauvegarde.append(mainTheme.mainColor.getBlue()).append("|");
        sauvegarde.append(mainTheme.secondaryColor.getRed()).append("|");
        sauvegarde.append(mainTheme.secondaryColor.getGreen()).append("|");
        sauvegarde.append(mainTheme.secondaryColor.getBlue()).append("|");
        sauvegarde.append(mainTheme.tertiaryColor.getRed()).append("|");
        sauvegarde.append(mainTheme.tertiaryColor.getGreen()).append("|");
        sauvegarde.append(mainTheme.tertiaryColor.getBlue()).append("|");
        sauvegarde.append(":Personnage:");
        for (Personnage p : allPersonnages.values()) {
            sauvegarde.append(p.name).append("|");
            sauvegarde.append(p.path).append("|");
            sauvegarde.append(p.description.replace("\n", "\\n")).append("|");
        }
        return sauvegarde.toString();
    }

    public void setMainFontType(Font font, String police) {
        font = new Font(police, font.getStyle(), font.getSize());
    }
    public void setMainFontStyle(Font font, int style) {
        font = new Font(font.getFontName(), style, font.getSize());
    }
    public void setMainFontSize(Font font, int size) {
        font = new Font(font.getFontName(), font.getStyle(), size);
    }
}
