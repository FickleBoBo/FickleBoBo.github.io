package pack1;

public class Test2 {

    private final Animal[] animals;

    public Test2(Animal... animals) {
        this.animals = new Animal[animals.length];
        for (int i = 0; i < animals.length; i++) {
            this.animals[i] = animals[i];
        }
    }

    public void func() {
        for (Animal animal : animals) {
            animal.bark();
        }
    }
}
