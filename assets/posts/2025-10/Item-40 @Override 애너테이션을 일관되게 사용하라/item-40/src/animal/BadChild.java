package animal;

public class BadChild extends Parent {

    // 메서드명 오타
    public void great() {
        System.out.println("BadChild.great");
    }

    // 파라미터 타입 불일치
    public void print(Object msg) {
        System.out.println("BadChild.print : " + msg);
    }

    // 파라미터 수 불일치
    public void print(String msg1, String msg2, String msg3) {
        System.out.println("BadChild.print : " + msg1 + " / " + msg2 + " / " + msg3);
    }
}
