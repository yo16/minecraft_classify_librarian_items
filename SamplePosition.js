import { useState } from "react";

import "./SamplePosition.css";

const POSITION = [
    ["水生特効5",   null,           "防具貫通4",        "重撃5"],
    ["忠誠3",       "水中呼吸3",    "フレイム",         "ノックバック1"],
    ["入れ食い3",   "水中歩行3",    "無限",             "ノックバック2"],
    ["宝釣り3",     "水中採掘",     "射撃ダメージ増加5","アンデッド特効5"],
    [null,          null,           null,               "火属性2"],
    ["幸運3",       "棘の鎧3",      null,               "ドロップ増加3"],
    ["シルクタッチ","落下耐性4",    "耐久力3",          "範囲ダメージ増加3"],
    ["効率強化5",   "ダメージ軽減4","修繕",             "ダメージ増加5"],
];

const SamplePosition = () => {
    const [isClicked, setIsClicked] = useState(
        [...Array(POSITION.length*4)].reduce(
            (m, v, i) => (
                {...m, [i]:false}
            ),{}
        )
    );

    const handleOnClick = (target, row, col) => {
        const orgIsClicked = {...isClicked};
        const newValue = !isClicked[row*4 + col];
        orgIsClicked[row*4 + col] = newValue;
        setIsClicked(orgIsClicked);
        
        target.style.backgroundColor = newValue?"#e66":"unset";
    }

    return (
        <div>
            <table className="tbl-position">
                <tbody>
                    {POSITION.map((line, i) => (
                        <tr key={`sample_tr_${i}`}>
                            <td
                                className="text-right"
                                onClick={(e)=>{handleOnClick(e.target, i,0);}}
                            >{line[0]?line[0]:""}</td>
                            <td
                                onClick={(e)=>{handleOnClick(e.target, i,1);}}
                            >{line[1]?line[1]:""}</td>
                            <td
                                className="text-right"
                                onClick={(e)=>{handleOnClick(e.target, i,2);}}
                            >{line[2]?line[2]:""}</td>
                            <td
                                onClick={(e)=>{handleOnClick(e.target, i,3);}}
                            >{line[3]?line[3]:""}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default SamplePosition;
