package pack1;

public class Dog implements Animal {
    String name;

    public Dog(String name) {
        this.name = name;
    }

    @Override
    public void bark() {
        System.out.println(name + " barked");
    }
}
