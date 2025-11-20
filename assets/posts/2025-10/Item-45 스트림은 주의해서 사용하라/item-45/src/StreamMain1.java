import java.util.List;
import java.util.stream.Stream;

public class StreamMain1 {
    public static void main(String[] args) {
        List<String> names = List.of("Apple", "Banana", "Berry", "Tomato");

        // 스트림의 생성
        Stream<String> stream = names.stream();

        // 중간 연산과 종단 연산
        stream
                .filter(name -> name.startsWith("B"))  // 중간 연산
                .map(name -> name.toUpperCase())  // 중간 연산
                .forEach(name -> System.out.println(name));  // 종단 연산

        // 출력 결과
        // BANANA
        // BERRY
    }
}
