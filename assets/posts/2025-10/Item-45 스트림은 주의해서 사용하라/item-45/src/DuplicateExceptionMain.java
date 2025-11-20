import java.util.stream.Stream;

public class DuplicateExceptionMain {
    public static void main(String[] args) {
        Stream<Integer> stream = Stream.of(1, 2, 3);

        stream.forEach(System.out::println);
        // 출력 결과
        // 1
        // 2
        // 3

        // IllegalStateException - stream has already been operated upon or closed
//        stream.forEach(System.out::println);
    }
}
