package javaTemplate;

import javaTemplate.Model.Environment;
import javaTemplate.Model.Instruction;
import javaTemplate.Model.SensorData;
import javaTemplate.Model.VisualizationData;

public class Solution {
    public class Result {
        private Instruction instruction;
        private VisualizationData visualizationData;

        public Result(Instruction instruction) {
            this.instruction = instruction;
            this.visualizationData = null;
        }

        public Result(Instruction instruction, VisualizationData visualizationData) {
            this.instruction = instruction;
            this.visualizationData = visualizationData;
        }

        public Instruction getInstruction() {
            return this.instruction;
        }

        public VisualizationData getVisualizationData() {
            return this.visualizationData;
        }

        @Override
        public String toString() {
            return Integer.toString(this.instruction.ordinal());
        }
    }

    public Solution(Environment env) {
        // Implement this if you want to do some precalculations
    }

    public Result getInstruction(SensorData data) {
        // Implement this function if you want to solve the second easier variation or
        // the complete task
        return new Result(Instruction.UP);
    }

    public Result getInstructionGPS(int x, int y) {
        // Implement this function if you want to solve only first easier variation of
        // the task
        return new Result(Instruction.UP);
    }
}