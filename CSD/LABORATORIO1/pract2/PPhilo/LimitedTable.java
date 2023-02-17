// CSD Mar 2013 Juansa Sendra

public class LimitedTable extends RegularTable { //max 4 in dinning-room
    public LimitedTable(StateManager state) {super(state);}
    int cont = 0;
    public synchronized void enter(int id) throws InterruptedException {
        cont++;
        while (cont == 5) { state.wenter(id); wait(); }
        state.enter(id);
    }
    public synchronized void exit(int id)  {
        cont--;
        state.exit(id);
        notifyAll();
    }
}
