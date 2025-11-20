public class ArrayCovariantTestMain {

    public static void main(String[] args) {
        Integer[] integers = new Integer[1];
        Object[] objects = integers;

//        objects[0] = "hello";
        // ArrayStoreException 발생
    }
}
