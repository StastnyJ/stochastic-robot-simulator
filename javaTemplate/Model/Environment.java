package javaTemplate.Model;

import java.util.ArrayList;
import java.util.List;

public class Environment {
    public static class Position {
        private SpotType type;
        private Float reward;

        public Position(SpotType type, Float reward) {
            this.type = type;
            this.reward = reward;
        }

        public SpotType getType() {
            return this.type;
        }

        public Float getReward() {
            return this.reward;
        }

        public static Position parsePosition(String raw) {
            if (raw.charAt(0) == '0')
                return new Position(SpotType.FREE_PLACE, 0.0f);
            else if (raw.charAt(0) == '1')
                return new Position(SpotType.WALL, 0.0f);
            else
                return new Position(SpotType.TERMINAL, Float.parseFloat(raw.substring(1)));
        }
    }

    private List<List<Position>> map;
    private Float stepPenalty;

    public Environment(List<List<Position>> map, Float stepPenalty) {
        this.map = map;
        this.stepPenalty = stepPenalty;
    }

    public List<List<Position>> getMap() {
        return this.map;
    }

    public Float getStepPenalty() {
        return this.stepPenalty;
    }

    public static Environment parseEnvironment(String raw) {
        String[] splited = raw.split(";");
        Float penalty = Float.parseFloat(splited[0]);
        Integer w = Integer.parseInt(splited[2]);
        String[] rawMap = splited[3].split(",");
        List<List<Position>> map = new ArrayList<>();
        List<Position> row = null;
        for (int i = 0; i < rawMap.length; i++) {
            if (i % w == 0) {
                if (i != 0)
                    map.add(row);
                row = new ArrayList<>();
            }
            row.add(Position.parsePosition(rawMap[i]));
        }
        return new Environment(map, penalty);
    }
}
