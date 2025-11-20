import java.util.List;

public class LazyEvalMain3 {
    public static void main(String[] args) {
        List<Integer> list = List.of(1, 2, 3, 4, 5, 6);

        Integer result = list.stream()
                .filter(i -> {
                    boolean isEven = i % 2 == 0;
                    System.out.println("filter() 실행: " + i + "(" + isEven + ")");
                    return isEven;
                })
                .map(i -> {
                    int mapped = i * 10;
                    System.out.println("map() 실행: " + i + "(" + mapped + ")");
                    return mapped;
                })
                .findFirst()
                .get();

        System.out.println("result = " + result);  // result = 20
    }
}
