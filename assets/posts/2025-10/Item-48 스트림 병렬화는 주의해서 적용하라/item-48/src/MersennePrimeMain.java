import java.math.BigInteger;
import java.util.stream.Stream;

import static java.math.BigInteger.*;

public class MersennePrimeMain {
    public static void main(String[] args) {
        long start = System.currentTimeMillis();

        primes().map(p -> TWO.pow(p.intValueExact()).subtract(ONE)) // 2^p-1로 매핑
                .filter(mersenne -> mersenne.isProbablePrime(50))  // 소수 여부를 판별
                .limit(20)  // 20개만
                .forEach(System.out::println);  // 출력

        long end = System.currentTimeMillis();
        System.out.println("Total time: " + (end - start) + "ms");  // Total time: 3447ms
    }

    private static Stream<BigInteger> primes() {
        return Stream.iterate(TWO, BigInteger::nextProbablePrime);
    }
}
