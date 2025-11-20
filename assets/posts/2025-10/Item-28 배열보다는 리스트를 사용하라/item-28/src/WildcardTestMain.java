import animal.Animal;
import animal.Cat;
import animal.Dog;

import java.util.ArrayList;
import java.util.List;

public class WildcardTestMain {

    public static void main(String[] args) {
        List<Dog> dogs = List.of(new Dog("개1"), new Dog("개2"), new Dog("개3"));
        List<Cat> cats = List.of(new Cat("고양이1"), new Cat("고양이2"), new Cat("고양이3"));

        List<Animal> animals = new ArrayList<>();
        addAll(dogs, animals);
        addAll(cats, animals);

        barkAll(animals);

        List<Object> objectList = new ArrayList<>();
        addAll(dogs, objectList);
        addAll(cats, objectList);

        for (Object object : objectList) {
            System.out.println(object);
        }
    }

    private static void barkAll(List<Animal> list) {
        for (Animal animal : list) {
            animal.bark();
        }
    }

    private static void addAll(List<? extends Animal> list, List<? super Animal> list2) {
        for (Animal animal : list) {
            list2.add(animal);
        }
    }
}
