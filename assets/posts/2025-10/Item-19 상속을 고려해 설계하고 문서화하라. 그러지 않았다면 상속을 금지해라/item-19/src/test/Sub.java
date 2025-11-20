package test;

import java.time.Instant;

public class Sub extends Super {

    private final Instant instant;

    public Sub() {
        System.out.println("Sub.Sub");
        instant = Instant.now();
    }

    @Override
    public void override() {
        System.out.println("Sub.override");
        System.out.println(instant);
    }
}
