import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class PrintUtilV3Main {

    public static void main(String[] args) throws NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
        PrintUtilV3.print("hello java V3");  // hello java V3

        /*
         * private 생성자 덕분에 외부에서 인스턴스화하는 것을 방지할 수 있다.
         * 또한 이를 상속 받고자 하는 클래스가 부모 클래스의 생성자(super())를 호출할 수 없어서 상속을 통한 인스턴스화도 방지된다.
         */
//        PrintUtilV3 p3 = new PrintUtilV3();

        // 리플렉션으로 만들 수 있기도 함
        Class<PrintUtilV3> clazz = PrintUtilV3.class;  // PrintUtilV3의 Class 객체를 가져옴
        Constructor<PrintUtilV3> cons = clazz.getDeclaredConstructor();  // 기본 생성자를 가져옴(접근 제어자에 상관없이)
        cons.setAccessible(true);  // private에 접근하는 설정
        PrintUtilV3 p3 = cons.newInstance();  // 인스턴스 생성

        System.out.println("p3 = " + p3);  // p3 = PrintUtilV3@5f184fc6
        System.out.println("p3.info = " + p3.info);  // p3.info = PrintUtilV3
    }
}
