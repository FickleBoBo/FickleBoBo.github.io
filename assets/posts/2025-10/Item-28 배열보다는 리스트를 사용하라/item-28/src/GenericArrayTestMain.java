import java.util.ArrayList;
import java.util.List;

public class GenericArrayTestMain {

    public static void main(String[] args) {
        List<Integer>[] adj = new ArrayList[1];
        // 로 타입 ArrayList 배열

        List<Object> objectList = new ArrayList<>();
        objectList.add("hello");
        // "hello" 하나를 원소로 갖는 List<Object>

        Object[] objectArray = adj;
        // 배열은 공변이라서 리스트 배열을 오브젝트 배열에 대입 가능

        objectArray[0] = objectList;
        // 오브젝트 배열에 objectList 대입

        Integer integer = adj[0].get(0);
        // Integer 타입 원소를 꺼낼 것으로 예상했지만 "hello"가 들어있어서 ClassCastException 발생
    }
}
