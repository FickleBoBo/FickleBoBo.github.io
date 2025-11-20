public class PrintUtilV4 {

    private PrintUtilV4() {
    }

    public static void print(String msg) {
        // private 생성자여도 해당 클래스 내부에서는 호출할 수 있으니 이것도 완전히 막으려면 예외를 던지자
        PrintUtilV4 p4 = new PrintUtilV4();
        System.out.println("p4 = " + p4);
        System.out.println(msg);
    }
}
