package javaTemplate;

import javaTemplate.Model.Environment;
import javaTemplate.Model.Instruction;
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

    }

    public Result getInstruction() {
        return new Result(Instruction.UP);
    }

    public Result getInstructionGPS() {
        return new Result(Instruction.UP);
    }
}