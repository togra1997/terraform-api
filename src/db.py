from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


class Database:
    def __init__(self, db_path: Path | str) -> None:
        """
        データベースを初期化します。

        Args:
            db_path (Path): データベースファイルのパス。
        """
        if not isinstance(db_path, Path):
            db_path = Path(db_path)
        self.db_path = db_path
        if db_path.exists():
            self.df = pd.read_csv(db_path)
        else:
            db_path.parent.mkdir(parents=True, exist_ok=True)
            self.df = pd.DataFrame(
                columns=[
                    "id",
                    "profile",
                    "vm_id",
                    "name",
                    "storage",
                    "memory",
                    "disk",
                    "ip",
                    "started",
                ]
            )

    def add(self, record: Dict[str, Any]) -> None:
        """
        レコードをデータベースに追加します。

        Args:
            record (Dict[str, Any]): 追加するレコードのデータ。

        Raises:
            ValueError: VM IDが既に存在する場合。
        """
        id = self.df["id"].max() + 1 if not self.df.empty else 1
        record["id"] = id
        if record["vm_id"] in self.df["vm_id"].to_numpy():
            raise ValueError(f"VM ID {record['vm_id']} already exists in the database.")

        self.df = pd.concat([self.df, pd.DataFrame([record])])

    def delete(self, vm_id: int) -> None:
        """
        指定されたVM IDのレコードを削除します。

        Args:
            vm_id (int): 削除するVM ID。

        Raises:
            ValueError: 指定されたVM IDが存在しない場合。
        """
        if vm_id not in self.df["vm_id"].to_numpy():
            raise ValueError(f"VM ID {vm_id} does not exist in the database.")
        self.df = self.df[self.df["vm_id"] != vm_id]

    def get(self) -> List[Any]:
        """
        データベースの内容をリスト形式で取得します。

        Returns:
            List[Any]: データベースの内容。
        """
        return self.df.drop(columns=["id"]).to_dict(orient="records")

    def save(
        self,
    ) -> None:
        """
        データベースをファイルに保存します。

        Args:
            db_path (Path): 保存先のファイルパス。
        """
        self.df.to_csv(self.db_path, index=False)


if __name__ == "__main__":
    db_path = Path("datas/database.csv")
    db = Database(db_path)
    db.add(
        {
            "profile": "minecraft",
            "vm_id": 150,
            "name": "minecraft",
            "storage": "sub-directory",
            "memory": 16384,
            "disk": 500,
            "ip": "192.168.112.22",
            "started": False,
        }
    )
    print(db.get())
    db.delete(150)
    db.save(db_path)
