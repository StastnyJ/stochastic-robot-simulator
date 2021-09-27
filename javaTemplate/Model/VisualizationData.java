package javaTemplate.Model;

import java.util.List;

public class VisualizationData {
    public class Color {
        private Integer red;
        private Integer green;
        private Integer blue;

        public Color(Integer red, Integer green, Integer blue) {
            this.red = red;
            this.green = green;
            this.blue = blue;
        }

        public Integer getRed() {
            return this.red;
        }

        public Integer getGreen() {
            return this.green;
        }

        public Integer getBlue() {
            return this.blue;
        }
    }

    private List<List<Color>> colors;
    private List<List<String>> texts;

    public VisualizationData(List<List<Color>> colors, List<List<String>> texts) {
        this.colors = colors;
        this.texts = texts;
    }

    public List<List<Color>> getColors() {
        return this.colors;
    }

    public List<List<String>> getTexts() {
        return this.texts;
    }
}
