import java.math.BigInteger;
import java.util.concurrent.ForkJoinPool;
import java.util.stream.LongStream;

public class PiMain2 {

    private static long num = 15L;

    public static void main(String[] args) {
        // JVM이 인식한 코어 수
        System.out.println("processorCount = " + Runtime.getRuntime().availableProcessors());

        // 공용 Fork-Join 풀의 워커 스레드의 수(보통 코어 수 - 1)
        System.out.println("commonPool = " + ForkJoinPool.commonPool().getParallelism());

        System.out.println("cnt = " + pi2(num));
    }

    private static long pi2(long n) {
        return LongStream.rangeClosed(2, n)
                .parallel()
                .mapToObj(BigInteger::valueOf)
                .filter(i -> i.isProbablePrime(50))
                .filter(i -> {
                    System.out.println(Thread.currentThread().getName() + " : " + i);
                    return true;
                })
                .count();
    }
}
