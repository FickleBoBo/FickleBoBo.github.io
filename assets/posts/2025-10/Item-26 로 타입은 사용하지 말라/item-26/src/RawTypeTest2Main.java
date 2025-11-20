import java.util.ArrayList;
import java.util.List;

public class RawTypeTest2Main {

    public static void main(String[] args) {
        List<String> stringList = new ArrayList<>();

        unsafeAdd(stringList, 1);
        String s = stringList.get(0);
        // ClassCastException 발생 -> 컴파일 타임에 잡지 못한다

//        errorAdd(stringList, 1);
        // List<String>은 List<Object>의 하위 타입이 아니라서 컴파일 에러 발생

//        safeAdd(stringList, 1);
        // 제네릭 메서드를 활용해 타입 안전성을 챙기면서 타입 별로 메서드 오버로딩을 하지 않아도 된다
    }

    private static void unsafeAdd(List list, Object o) {
        list.add(o);
    }

    private static void errorAdd(List<Object> list, Object o) {
        list.add(o);
    }

    private static <E> void safeAdd(List<E> list, E e) {
        list.add(e);
    }
}
