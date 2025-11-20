import animal.BadChild;
import animal.GoodChild;
import animal.Parent;

public class Main {

    public static void main(String[] args) {
        Parent p = new BadChild();
        p.greet();
        p.print("hello");
        p.print("hello", "java");
        // Parent.greet
        // Parent.print : hello
        // Parent.print : hello / java

        Parent p2 = new GoodChild();
        p2.greet();
        p2.print("hello");
        p2.print("hello", "java");
        // GoodChild.greet
        // GoodChild.print : hello
        // GoodChild.print : hello / java

    }
}
