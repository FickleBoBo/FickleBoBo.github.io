public class PrintUtilV2Main {

    public static void main(String[] args) {
        PrintUtilV2.print("hello java V2");  // hello java V2

        // 추상 클래스로 선언해서 인스턴스화를 방지할 수 있다.
//        PrintUtilV2 p2 = new PrintUtilV2();

        // 하지만 상속 받아서 인스턴스화할 수 있고 추상 클래스로 선언하면 상속 받아 사용하라는 의도로 비춰질 수 있다.
        PrintUtilV2 p2 = new PrintUtilV2Child();
        System.out.println("p2.info = " + p2.info);  // p2.info = PrintUtilV2

        PrintUtilV2Child p3 = (PrintUtilV2Child) p2;
        System.out.println("p3.info = " + p3.info);  // p3.info = PrintUtilV2Child

        // 물론 익명 클래스로도 인스턴스화가 가능하다.(추상 메서드가 없어서 본문은 비움)
        PrintUtilV2 p4 = new PrintUtilV2() {
        };

        System.out.println("p4 = " + p4);  // p4 = PrintUtilV2Main$1@723279cf
        System.out.println("p4.info = " + p4.info);  // p4.info = PrintUtilV2
    }
}
