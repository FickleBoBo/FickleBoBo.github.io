package animal;

public class Cat implements Animal {

    public String name;

    public Cat(String name) {
        this.name = name;
    }

    @Override
    public void bark() {
        System.out.println(name + " 냐옹");
    }

    @Override
    public String toString() {
        return "Cat{" +
                "name='" + name + '\'' +
                '}';
    }
}
