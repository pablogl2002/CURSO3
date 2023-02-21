// CSD feb 2015 Juansa Sendra

public class Pool1 extends Pool {   //no kids alone
    int nInst = 0;
    int nKids = 0;
    
    public void init(int ki, int cap)           {}
    public synchronized void kidSwims() throws InterruptedException {
        while (nInst <= 0) {
            log.waitingToSwim();
            wait();
        }
        nKids++;
        notifyAll();
        log.swimming();
    }
    public synchronized void kidRests()      {
        nKids--;
        log.resting();
        notifyAll();
    }
    public synchronized void instructorSwims()   {
        nInst++;
        log.swimming();
        notifyAll();
    }
    public synchronized void instructorRests() throws InterruptedException {
        while (nKids > 0 && nInst == 1) {
            log.waitingToRest();
            wait();
        }
        nInst--;
        log.resting();
        notifyAll();
    }
}
