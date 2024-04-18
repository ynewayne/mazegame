import java.awt.Desktop;
import java.net.URI;

public class FlaskLauncher {
    public static void main(String[] args) {
        // Flask server URL
        String flaskUrl = "http://localhost:5000"; // Adjust the URL as needed

        // Open default browser and navigate to Flask URL
        try {
            Desktop.getDesktop().browse(new URI(flaskUrl));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
