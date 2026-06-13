import java.applet.Applet;
import java.applet.*;
import java.awt.*;

public class AppletLifeCycleDemo extends Applet {
    // Initialization phase
    public void init() {
        System.out.println("Applet initialized");
    }

    // Starting phase
    public void start() {
        System.out.println("Applet started");
    }

    // Painting phase
    public void paint(Graphics g) {
        System.out.println("Applet painting");
        g.drawString("Hello, World!", 20, 20);
    }

    // Stopping phase
    public void stop() {
        System.out.println("Applet stopped");
    }

    // Destruction phase
    public void destroy() {
        System.out.println("Applet destroyed");
    }
}
