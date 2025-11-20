import operation.BasicOperation;
import operation.ExtendedOperation;
import operation.Operation;

public class Main {

    public static void main(String[] args) {
        double x = 2;
        double y = 4;

        printAll(BasicOperation.class, x, y);
        // 2.0 + 4.0 = 6.0
        // 2.0 - 4.0 = -2.0
        // 2.0 * 4.0 = 8.0
        // 2.0 / 4.0 = 0.5
        printAll(ExtendedOperation.class, x, y);
        // 2.0 ^ 4.0 = 16.0
        // 2.0 % 4.0 = 2.0
    }

    private static <T extends Enum<T> & Operation> void printAll(Class<T> enumType, double x, double y) {
        for (Operation op : enumType.getEnumConstants()) {
            System.out.println(x + " " + op + " " + y + " = " + op.apply(x, y));
        }
    }
}
