import animal.Animal;
import animal.Dog;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class ListMethodTestMain {

    public static void main(String[] args) {
        List<Dog> dogs = new ArrayList<>();
        dogs.add(new Dog("개1"));
        dogs.add(new Dog("개3"));
        dogs.add(new Dog("개4"));
        dogs.add(new Dog("개2"));
        dogs.add(new Dog("개5"));

        List<Animal> animals = new ArrayList<>(dogs);
        for (Animal animal : animals) {
            System.out.println(animal);
        }
        // Dog{name='개1'}
        // Dog{name='개3'}
        // Dog{name='개4'}
        // Dog{name='개2'}
        // Dog{name='개5'}

        Comparator<Animal> animalComparator = new Comparator<>() {
            @Override
            public int compare(Animal o1, Animal o2) {
                return -1;
            }
        };

        dogs.sort(animalComparator);
        for (Dog dog : dogs) {
            System.out.println(dog);
        }
        // Dog{name='개5'}
        // Dog{name='개2'}
        // Dog{name='개4'}
        // Dog{name='개3'}
        // Dog{name='개1'}
    }
}
