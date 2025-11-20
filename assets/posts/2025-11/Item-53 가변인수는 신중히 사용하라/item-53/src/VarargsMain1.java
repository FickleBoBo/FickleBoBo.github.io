public class VarargsMain1 {
    public static void main(String[] args) {
        int result1 = sum();
        int result2 = sum(1);
        int result3 = sum(1, 2, 3);

        System.out.println("result1 = " + result1);  // result1 = 0
        System.out.println("result2 = " + result2);  // result2 = 1
        System.out.println("result3 = " + result3);  // result3 = 6
    }

    static int sum(int... args) {
        int sum = 0;
        for (int arg : args) {
            sum += arg;
        }
        return sum;
    }
}
