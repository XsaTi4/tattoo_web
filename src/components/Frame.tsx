import styles from './Frame.module.css';

interface FrameProps {
    children: React.ReactNode;
    className?: string;
    hideBottom?: boolean;
}

export default function Frame({ children, className = '', hideBottom = false }: FrameProps) {
    return (
        <div className={`${styles.frame} ${className} ${hideBottom ? styles.hideBottom : ''}`}>
            <div className={styles.cornerTopLeft}></div>
            <div className={styles.cornerTopRight}></div>
            <div className={`${styles.cornerBottomLeft} ${hideBottom ? styles.hideBottomCorner : ''}`}></div>
            <div className={`${styles.cornerBottomRight} ${hideBottom ? styles.hideBottomCorner : ''}`}></div>
            <div className={styles.content}>
                {children}
            </div>
        </div>
    );
}
