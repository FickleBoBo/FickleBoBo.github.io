package animal;

public class Parent {

    public void greet() {
        System.out.println("Parent.greet");
    }

    public void print(String msg) {
        System.out.println("Parent.print : " + msg);
    }

    public void print(String msg1, String msg2) {
        System.out.println("Parent.print : " + msg1 + " / " + msg2);
    }
}
