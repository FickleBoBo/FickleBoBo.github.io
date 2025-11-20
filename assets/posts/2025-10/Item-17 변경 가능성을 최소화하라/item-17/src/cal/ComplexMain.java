package cal;

public class ComplexMain {

    public static void main(String[] args) {
        Complex c1 = new Complex(1.0, 1.0);
        Complex c2 = new Complex(2.0, -2.0);

        Complex ans1 = c1.plus(c2);
        System.out.println("ans1 = " + ans1);  // ans1 = Complex{re=3.0, im=-1.0}

        Complex ans2 = c1.plus(c1).plus(c1).plus(c1);  // ans2 = Complex{re=4.0, im=4.0}
        System.out.println("ans2 = " + ans2);
    }
}
