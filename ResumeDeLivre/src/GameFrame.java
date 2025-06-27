import javax.swing.*;
import java.awt.*;

public class GameFrame extends JFrame {

    GameFrame(String[] args) {
        GamePanel gp = new GamePanel(args);
        this.add(gp);
        this.setTitle("Sorted");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setResizable(true);
        this.pack();
        this.setMinimumSize(new Dimension(640, 360));
        this.setMaximumSize(new Dimension(1920, 1080));
        this.setVisible(true);
        this.setLocationRelativeTo(null);
        this.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
    }
}
