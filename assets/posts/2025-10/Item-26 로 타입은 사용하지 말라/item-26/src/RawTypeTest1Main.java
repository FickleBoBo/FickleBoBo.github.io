import java.util.ArrayList;
import java.util.List;

public class RawTypeTest1Main {

    public static void main(String[] args) {
        List numberList = new ArrayList();

        numberList.add(1);
        numberList.add('1');
        numberList.add("1");

        // iter로 순회하면 Object 타입으로 꺼내짐
        for (Object o : numberList) {
            System.out.println(o);
        }

        // 출력 결과
        // 1
        // 1
        // 1
    }
}
