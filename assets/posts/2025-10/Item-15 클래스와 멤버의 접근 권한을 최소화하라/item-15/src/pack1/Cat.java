package pack1;

public class Cat implements Animal {
    String name;

    public Cat(String name) {
        this.name = name;
    }

    @Override
    public void bark() {
        System.out.println(name + " barked");
    }
}
