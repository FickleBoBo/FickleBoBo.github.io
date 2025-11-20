package advanced;

import java.util.List;

public class Main {

    public static void main(String[] args) {
        Favorites f = new Favorites();

        List<Integer> integerList = List.of(1, 2, 3, 4, 5);
        List<String> stringList = List.of("a", "b", "c", "d", "e", "f");

        f.putFavorite(List.class, integerList);  // List<Integer>.class 불가
        f.putFavorite(List.class, stringList);  // List<String>.class 불가

        List favorite = f.getFavorite(List.class);

        System.out.println(favorite);
        // 출력 결과
        // [a, b, c, d, e, f]
    }
}
