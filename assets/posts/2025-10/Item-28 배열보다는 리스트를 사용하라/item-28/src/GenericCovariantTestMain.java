import java.util.ArrayList;
import java.util.List;

public class GenericCovariantTestMain {

    public static void main(String[] args) {
        List<Integer> integerList = new ArrayList<>();
//        List<Object> objectList = integerList;  // 컴파일 실패
    }
}
