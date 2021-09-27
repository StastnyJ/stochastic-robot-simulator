package javaTemplate.Model;

public class SensorData {
    private Boolean up;
    private Boolean left;
    private Boolean right;
    private Boolean down;

    public SensorData(Boolean up, Boolean left, Boolean right, Boolean down) {
        this.up = up;
        this.left = left;
        this.right = right;
        this.down = down;
    }

    public static SensorData parseSensorData(String raw) {
        String[] splited = raw.split(";");
        return new SensorData(Boolean.parseBoolean(splited[0]), Boolean.parseBoolean(splited[1]),
                Boolean.parseBoolean(splited[2]), Boolean.parseBoolean(splited[3]));
    }

    public Boolean getUp() {
        return this.up;
    }

    public Boolean isUp() {
        return this.up;
    }

    public Boolean getLeft() {
        return this.left;
    }

    public Boolean isLeft() {
        return this.left;
    }

    public Boolean getRight() {
        return this.right;
    }

    public Boolean isRight() {
        return this.right;
    }

    public Boolean getDown() {
        return this.down;
    }

    public Boolean isDown() {
        return this.down;
    }

}
