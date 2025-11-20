package collection;

import java.util.HashSet;
import java.util.Set;

public class UserMain {

    public static void main(String[] args) {
        Set<User> users = new HashSet<>();

        User user1 = new User("bobo");
        users.add(user1);
        System.out.println("users.size() = " + users.size());  // users.size() = 1

        user1.name = "bobo2";
        User user2 = new User("bobo2");
        users.add(user2);
        System.out.println("users.size() = " + users.size());  // users.size() = 2

        User user3 = new User("bobo2");
        users.add(user3);
        System.out.println("users.size() = " + users.size());  // users.size() = 2

        users.forEach(System.out::println);
        // User{name='bobo2'}
        // User{name='bobo2'}
    }
}
