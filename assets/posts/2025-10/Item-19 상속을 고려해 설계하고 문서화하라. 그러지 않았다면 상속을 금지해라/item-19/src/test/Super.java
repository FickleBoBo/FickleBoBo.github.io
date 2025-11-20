package test;

public class Super {

    public Super() {
        System.out.println("Super.Super");
        override();
    }

    public void override() {
        System.out.println("Super.override");
    }
}
