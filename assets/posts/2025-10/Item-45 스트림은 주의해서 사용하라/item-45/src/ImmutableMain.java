import java.util.List;

public class ImmutableMain {
    public static void main(String[] args) {
        List<Integer> originList = List.of(1, 2, 3, 4, 5);
        System.out.println("originList = " + originList);  // originList = [1, 2, 3, 4, 5]

        List<Integer> filteredList = originList.stream()
                .filter(n -> n % 2 == 0)
                .toList();
        System.out.println("filteredList = " + filteredList);  // filteredList = [2, 4]
        System.out.println("originList = " + originList);  // originList = [1, 2, 3, 4, 5]
    }
}
