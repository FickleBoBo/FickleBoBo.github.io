import java.math.BigInteger;
import java.util.stream.LongStream;

public class PiMain {

    private static long start;
    private static long end;
    private static long num = 10_000_000L;

    public static void main(String[] args) {
        start = System.currentTimeMillis();
        System.out.println(pi1(num));
        end = System.currentTimeMillis();
        System.out.println("Total time: " + (end - start) + "ms");

        start = System.currentTimeMillis();
        System.out.println(pi2(num));
        end = System.currentTimeMillis();
        System.out.println("Total time: " + (end - start) + "ms");
    }

    private static long pi1(long n) {
        return LongStream.rangeClosed(2, n)
                .mapToObj(BigInteger::valueOf)
                .filter(i -> i.isProbablePrime(50))
                .count();
    }

    private static long pi2(long n) {
        return LongStream.rangeClosed(2, n)
                .parallel()
                .mapToObj(BigInteger::valueOf)
                .filter(i -> i.isProbablePrime(50))
                .count();
    }
}
