package animal;

public class GoodChild extends Parent {

    @Override
    public void greet() {
        System.out.println("GoodChild.greet");
    }

    @Override
    public void print(String msg) {
        System.out.println("GoodChild.print : " + msg);
    }

    @Override
    public void print(String msg1, String msg2) {
        System.out.println("GoodChild.print : " + msg1 + " / " + msg2);
    }
}
